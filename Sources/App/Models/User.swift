import FluentSQLite
import Vapor

struct User: SQLiteModel {
    
    var id: Int?
    
    var name: String
    
    var lastMsgTime: Int? = 0
    
    var feedURL: String
}

/// Allows `User` to be used as a dynamic migration.
extension User: Migration { }

/// Allows `User` to be encoded to and decoded from HTTP messages.
extension User: Content { }

/// Allows `User` to be used as a dynamic parameter in route definitions.
extension User: Parameter { }
