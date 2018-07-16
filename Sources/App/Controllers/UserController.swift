import Vapor

final class UserController: RouteCollection {
    
    func boot(router: Router) throws {
        let group = router.grouped("user")
        
        group.get("", use: index)
        group.post("", use: create)
        //        group.delete("", User.parameter, use: delete)
        group.get("status", String.parameter , use: status)
        group.get("logout", String.parameter, use: logout)
    }
}

extension UserController {
    
    func index(_ req: Request) throws -> Future<Response> {
        return User.query(on: req).all().flatMap { users in
            return try JSONResponse<[User]>(data: users).encode(for: req)
        }
    }
    
    func create(_ req: Request) throws -> Future<Response> {
        
        return try req.content.decode(User.self).flatMap { user in
            
            return User.query(on: req).filter(\.name, .equal, user.name).first()
                .flatMap { localUser -> Future<User> in
                    if var `localUser` = localUser {
                        localUser.feedURL = user.feedURL
                        localUser.isOnline = true
                        return localUser.save(on: req)
                    }
                    var `user` = user
                    user.isOnline = true
                    return user.save(on: req)
                }.flatMap { _ in try JSONResponse<Empty>(status: .ok).encode(for: req) }
        }
    }
    
    func delete(_ req: Request) throws -> Future<HTTPStatus> {
        return try req.parameters.next(User.self)
            .flatMap {
                $0.delete(on: req)
            }
            .transform(to: .ok)
    }
    
    func status(_ req: Request) throws -> Future<Response> {
        let username = try req.parameters.next(String.self)
        return User.query(on: req).filter(\.name, .equal, username)
            .first()
            .flatMap { user in
                let status = user == nil ? UserRegisterStatus(status: false, msg: "") : UserRegisterStatus(status: true, msg: "ok.")
                if var `user` = user {
                    user.isOnline = true
                    _ = user.save(on: req)
                }
                return try JSONResponse<UserRegisterStatus>(data: status).encode(for: req)
        }
    }
    
    func logout(_ req: Request) throws -> Future<Response> {
        let username = try req.parameters.next(String.self)
        return User.query(on: req).filter(\User.name, .equal, username)
            .first()
            .unwrap(or: ServiceError.init(identifier: "", reason: ""))
            .flatMap { user -> EventLoopFuture<User> in
                var `user` = user
                user.isOnline = false
                return user.save(on: req)
            }
            .flatMap { _ in
                return try JSONResponse<Empty>(status: .ok).encode(for: req)
            }
            .catchFlatMap { _ in try JSONResponse<Empty>(status: .ok).encode(for: req) }
    }
}

