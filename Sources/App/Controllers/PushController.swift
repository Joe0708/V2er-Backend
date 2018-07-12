import Vapor

final class PushController: RouteCollection {
    
    func boot(router: Router) throws {
        let group = router.grouped("user")
        
        group.get("", use: index)
        group.post("", use: create)
        group.delete("", User.parameter, use: delete)
    }
}

extension PushController {
    
    /// Returns a list of all `Todo`s.
    func index(_ req: Request) throws -> Future<Response> {
        return User.query(on: req).all().flatMap { users in
            return try JSONResponse<[User]>(data: users).encode(for: req)
        }
    }
    
    func create(_ req: Request) throws -> Future<Response> {
        return try req.content.decode(User.self).flatMap { user in
            return user.save(on: req)
                .flatMap { _ in try JSONResponse<Empty>(status: .ok).encode(for: req) }
        }
    }
    
    func delete(_ req: Request) throws -> Future<HTTPStatus> {
        return try req.parameters.next(User.self).flatMap { user in
            return user.delete(on: req)
            }.transform(to: .ok)
    }
}

