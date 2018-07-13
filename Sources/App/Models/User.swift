import FluentSQLite
import Vapor

/// A single entry of a Todo list.
struct User: SQLiteModel {

    var id: Int?
    
//    var userID: Int
    
    var name: String
    
    var lastMsgTime: Int? = 0
    
    var feedURL: String
}

/// Allows `Todo` to be used as a dynamic migration.
extension User: Migration { }

/// Allows `Todo` to be encoded to and decoded from HTTP messages.
extension User: Content { }

/// Allows `Todo` to be used as a dynamic parameter in route definitions.
extension User: Parameter { }

