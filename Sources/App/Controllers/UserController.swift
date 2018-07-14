import Vapor

final class UserController: RouteCollection {
    
    func boot(router: Router) throws {
        let group = router.grouped("user")
        
        group.get("", use: index)
        group.post("", use: create)
        group.delete("", User.parameter, use: delete)
        group.get("", User.parameter, use: delete)
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
                        return localUser.save(on: req)
                    }
                    return user.save(on: req)
                }.flatMap { _ in try JSONResponse<Empty>(status: .ok).encode(for: req) }
        }
    }
    
    func delete(_ req: Request) throws -> Future<HTTPStatus> {
        return try req.parameters.next(User.self)
            .flatMap { $0.delete(on: req) }
            .transform(to: .ok)
    }
}

