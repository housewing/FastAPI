user_sql = {
    'get_user': "SELECT id, username, password FROM [User] WHERE username = '{}'",
    'create_user': "INSERT INTO [User] (id, username, password) VALUES(?, ?, ?)",
}

note_sql = {
    'get_notes': "SELECT id, title, content FROM Note",
    'create_note': "INSERT INTO Note (id, title, content) VALUES(?, ?, ?)",
    'delete_note': "DELETE FROM Note WHERE id = '{}'"
}
