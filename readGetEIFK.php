<?php
$servername = "localhost";
$username = "id22104230_jcboisset";
$password = "Jcb27/*-+";
$database = "id22104230_jcboisset";

$conn = new mysqli($servername, $username, $password, $database);

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Retrieve data from GET request parameters
$TemperatureCBME680 = isset($_GET['TemperatureCBME680']) ? $_GET['TemperatureCBME680'] : 0.0;
$PressureHPaBME680 = isset($_GET['PressureHPaBME680']) ? $_GET['PressureHPaBME680'] : 0.0;
$HumidityPercentageBME680 = isset($_GET['HumidityPercentageBME680']) ? $_GET['HumidityPercentageBME680'] : 0.0;
$GasKOhmsBME680 = isset($_GET['GasKOhmsBME680']) ? $_GET['GasKOhmsBME680'] : 0.0;
$TemperatureCDH22 = isset($_GET['TemperatureCDH22']) ? $_GET['TemperatureCDH22'] : 0.0;
$humiPercentageDHT22 = isset($_GET['humiPercentageDHT22']) ? $_GET['humiPercentageDHT22'] : 0.0;
$dustDensityMgM3 = isset($_GET['dustDensityMgM3']) ? $_GET['dustDensityMgM3'] : 0.0;

// Get the server's current timestamp
//$timePresent = date('Y-m-d H:i:s');
date_default_timezone_set('Africa/Nairobi');
$timePresent = date('Y-m-d H:i:s');

// Prepare and bind the SQL statement
$sql = "INSERT INTO weatherEIFK (timePresent, TemperatureCBME680, PressureHPaBME680, HumidityPercentageBME680, GasKOhmsBME680, TemperatureCDH22, humiPercentageDHT22, dustDensityMgM3) VALUES (?, ?, ?, ?, ?, ?, ?, ?)";
$stmt = $conn->prepare($sql);
$stmt->bind_param("ssssssss", $timePresent, $TemperatureCBME680, $PressureHPaBME680, $HumidityPercentageBME680, $GasKOhmsBME680, $TemperatureCDH22, $humiPercentageDHT22, $dustDensityMgM3);

// Execute the prepared statement
if ($stmt->execute() === TRUE) {
    echo "Data inserted successfully";
} else {
    echo "Error: " . $stmt->error;
}

// Close the prepared statement and connection
$stmt->close();
$conn->close();
?>