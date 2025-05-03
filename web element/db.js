const sqlite3 = require('sqlite3').verbose();

/**
 * Initializes the database connection.
 * @param {string} dbPath - The path to the SQLite database file.
 * @returns {sqlite3.Database} - The database connection object.
 */
function initializeDatabase(dbPath) {
    return new sqlite3.Database(dbPath, (err) => {
        if (err) {
            console.error("Error connecting to database:", err.message);
        } else {
            console.log("Connected to database:", dbPath);
        }
    });
}

// Default database connection
const db = initializeDatabase('D:/Ching/VS code/SBA/database/Sports day helper.db');

/**
 * Executes a query on the SQLite database.
 * @param {string} query - The SQL query to execute.
 * @param {Array} params - The parameters for the query.
 * @returns {Promise} - Resolves with the query result.
 */
function executeQuery(query, params = []) {
    return new Promise((resolve, reject) => {
        db.run(query, params, function (err) {
            if (err) {
                reject(err);
            } else {
                resolve(this);
            }
        });
    });
}

/**
 * Fetches all rows from a query.
 * @param {string} query - The SQL query to execute.
 * @param {Array} params - The parameters for the query.
 * @returns {Promise<Array>} - Resolves with the rows.
 */
function fetchAll(query, params = []) {
    return new Promise((resolve, reject) => {
        db.all(query, params, (err, rows) => {
            if (err) {
                reject(err);
            } else {
                resolve(rows);
            }
        });
    });
}

/**
 * Fetches a single row from a query.
 * @param {string} query - The SQL query to execute.
 * @param {Array} params - The parameters for the query.
 * @returns {Promise<Object>} - Resolves with the row.
 */
function fetchOne(query, params = []) {
    return new Promise((resolve, reject) => {
        db.get(query, params, (err, row) => {
            if (err) {
                reject(err);
            } else {
                resolve(row);
            }
        });
    });
}

/**
 * Fetches user details by Gmail.
 * @param {string} gmail - The Gmail address to search for.
 * @returns {Promise<Object>} - Resolves with the user details.
 */
function fetchUserByGmail(gmail) {
    const query = "SELECT name, gender, dob, house FROM stu_info WHERE gmail = ?";
    return fetchOne(query, [gmail]);
}

module.exports = {
    initializeDatabase,
    executeQuery,
    fetchAll,
    fetchOne,
    fetchUserByGmail
};