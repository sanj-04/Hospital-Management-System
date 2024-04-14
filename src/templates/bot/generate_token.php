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
//$sql = "DROP TABLE IF EXISTS patient_tokens";
//$conn->query($sql);

// Recreate the patient_tokens table
//$sql = "CREATE TABLE IF NOT EXISTS patient_tokens (patient_id INTEGER PRIMARY KEY, token INTEGER UNIQUE)";
//$conn->query($sql);

// Get the patient ID from the AJAX request
$patientId = $_POST['patientId'];

// Query the database to check if the patient ID exists
$sql = "SELECT * FROM patientdetails WHERE patient_id = '$patientId'";
$result = $conn->query($sql);

if ($result->num_rows > 0) {
    // Call the Python script to generate the token number
    //$pythonScript = 'python token4.py ' . $patientId;
    //$tokenOutput = shell_exec($pythonScript);
    //$token=5;
    $rdate = date("Y-m-d");
    $sql= "SELECT token  from  tokentracker where rdate='$rdate' and patient_id='$patientId'";
    $result = $conn->query($sql);
    if ($result->num_rows > 0) {
        $row = $result->fetch_assoc();
        $token = $row['token'];
        echo "token already exists for this patient ".$token;

    }else{

    $sql= "SELECT MAX(token) AS max_token from  tokentracker where rdate='$rdate'";
    $result = $conn->query($sql);
    if ($result->num_rows > 0) {
        $row = $result->fetch_assoc();
        $max_token = $row['max_token'];
        $token=$max_token+1;
    }else{
        $token=1;
    }
    $sql="INSERT INTO tokentracker (patient_id, token, rdate) VALUES ('$patientId', '$token' ,'$rdate')";
    $result = $conn->query($sql);

echo "token generated successfully ".$token;
    }
} else {
    echo "Invalid patient ID";
}

$conn->close();
?>