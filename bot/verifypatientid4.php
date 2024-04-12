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

// Get the patient ID from the AJAX request
$patientId = $_POST['patientId'];

// Query the database to check if the patient ID exists
$sql = "SELECT * FROM patientdetails WHERE patient_id = '$patientId'";
$result = $conn->query($sql);

if ($result->num_rows > 0) {
    echo "Congratulations";
} else {
    echo "Invalid patient ID";
}

$conn->close();
?>