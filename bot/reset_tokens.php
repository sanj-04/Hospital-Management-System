<?php
// Database connection details
$servername = "localhost";
$username = "root";
$password = "";
$dbname = "patientrecords";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Drop the patient_tokens table if it exists
$sql = "DROP TABLE IF EXISTS patient_tokens";
if ($conn->query($sql) === TRUE) {
    echo "Patient tokens table dropped successfully";
} else {
    echo "Error dropping patient tokens table: " . $conn->error;
}

$conn->close();
?>