<?php
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

// Connect to the database
$servername = "localhost";
$username = "id22104230_jcboisset";
$password = "Jcb27/*-+";
$dbname = "id22104230_jcboisset";
$conn = new mysqli($servername, $username, $password, $dbname);

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

if (isset($_POST['start_date']) && isset($_POST['end_date'])) {
    $start_date = $_POST['start_date'];
    $end_date = $_POST['end_date'];
    $normalize = isset($_POST['normalize']) ? $_POST['normalize'] : 0;

    // Ensure dates are properly formatted to avoid SQL injection
    $start_date = $conn->real_escape_string($start_date);
    $end_date = $conn->real_escape_string($end_date);

    // Add time range to fetch data for the entire day
    $start_date .= ' 00:00:00';
    $end_date .= ' 23:59:59';

    $sql = "SELECT * FROM Weather WHERE TimePresent BETWEEN '$start_date' AND '$end_date' AND TemperatureC <> 0 AND PressureHPa <> 0 AND HumidityPercentage <> 0 AND GasKOhms <> 0";
    $result = $conn->query($sql);

    $data = array();
    if ($result->num_rows > 0) {
        while($row = $result->fetch_assoc()) {
            $data[] = $row;
        }

        if ($normalize) {
            // Get min and max values for each field
            $minTemp = min(array_column($data, 'TemperatureC'));
            $maxTemp = max(array_column($data, 'TemperatureC'));
            $minPressure = min(array_column($data, 'PressureHPa'));
            $maxPressure = max(array_column($data, 'PressureHPa'));
            $minHumidity = min(array_column($data, 'HumidityPercentage'));
            $maxHumidity = max(array_column($data, 'HumidityPercentage'));
            $minGas = min(array_column($data, 'GasKOhms'));
            $maxGas = max(array_column($data, 'GasKOhms'));

            // Normalize each row
            foreach ($data as &$row) {
                $row['NormalizedTemperature'] = ($row['TemperatureC'] - $minTemp) / ($maxTemp - $minTemp);
                $row['NormalizedPressure'] = ($row['PressureHPa'] - $minPressure) / ($maxPressure - $minPressure);
                $row['NormalizedHumidity'] = ($row['HumidityPercentage'] - $minHumidity) / ($maxHumidity - $minHumidity);
                $row['NormalizedGas'] = ($row['GasKOhms'] - $minGas) / ($maxGas - $minGas);
            }
        }
    }
    $conn->close();

    echo json_encode($data);
} else {
    echo json_encode([]);
}
?>