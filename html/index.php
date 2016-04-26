<!DOCTYPE>
<html>
<head>
	<meta http-equiv="content-type" content="text/html; charset=UTF-8">
	<meta http-equiv="refresh" content="10">
	<link rel="stylesheet" href="https://cdn.jsdelivr.net/foundation/6.2.1/foundation.min.css">
		<style>
			table {
				border: 2px solid rgba(50, 50, 50, 0.5);
			}
			table th {
				text-align: left;
			}
			.container {
				margin-top: 50px;
			}
			header h1 {
				font-size: 24px;
			}
		</style>
</head>
<body>

<div class="container">
	<div class="row">
		<div class="large-12 columns">
			<header class="primary callout">
				<h1>Palmbeach Kings - Data Log Page</h1>
				<p>This page shows data collected by the Palmbeach Kings group.</p>
			</header>
		</div>
	</div>
	<div class="row">
			<div class="large-6 columns">
				<?php
				$servername = 'palm-beach.czexil0tgoyr.us-east-1.rds.amazonaws.com';
				$username = 'palm';
				$password = 'palmbeach192';
				$dbname = 'data';
				$conn = new mysqli($servername, $username, $password, $dbname);

				if ($conn->connect_error) {
					die("Connection failed: " . $conn->connect_error);
				}
				$sql = "SELECT id, name, time FROM log ORDEr BY id desc LIMIT 5";
				$result = $conn->query($sql);
				if ($result->num_rows > 0) {

					echo "<table class='table'><tr><th>LOGIN HISTORY</th></tr><tr><th>ID</th><th>Name</th><th>Time</th></tr>";
					// output data of each row
					while($row = $result->fetch_assoc()) {
						echo "<tr><td>" . $row["id"]. "</td><td>" . $row["name"]. "</td><td>" . $row["time"]. "</td></tr>";
					}
					echo "</table>";
				} else {
					echo "0 results";
				}
				$conn->close();
				?>
			</div>
			<div class="large-6 columns">
				<?php

				$servername = 'palm-beach.czexil0tgoyr.us-east-1.rds.amazonaws.com';
				$username = 'palm';
				$password = 'palmbeach192';
				$dbname = 'data';
				$conn = new mysqli($servername, $username, $password, $dbname);

				$temperatures = array();
				$dates = array();
				$brightnesses = array();
				$avgTemperatures = array();
				$avgHourlyTemperatures = array();
				$avgHourlyTemperatureDates = array();
				$avgBrightnesses = array();
				$avgHourlyBrightnesses = array();
				$avgHourlyBrightnessDates = array();
				$avgTemperatureDates = array();
				$avgBrightnessDates = array();

				if ($conn->connect_error) {
					die("Connection failed: " . $conn->connect_error);
				}
				$sql = "SELECT id, temperature, brightness, date FROM data ORDEr BY id desc LIMIT 5";
				$result = $conn->query($sql);
				if ($result->num_rows > 0) {

					echo "<table class='table'><tr><th>DATA LOGS</th></tr><tr><th>ID</th><th>Temperature</th><th>Brightness</th><th>Date</th></tr>";

					while($row = $result->fetch_assoc()) {
						echo "<tr><td>" . $row["id"]. "</td><td>" . $row["temperature"]. "</td><td>" . $row["brightness"]. "</td><td>" . $row["date"]. "</td></tr>";
						// Add each value to the array. These arrays are used by the JS charts.
						$temperatures[] = $row["temperature"];
						$dates[] = $row["date"];
						$brightnesses[] = $row["brightness"];
					}
					echo "</table>";
				} else {
					echo "0 results";
				}
				$conn->close();
				?>

				<?php

				$servername = 'palm-beach.czexil0tgoyr.us-east-1.rds.amazonaws.com';
				$username = 'palm';
				$password = 'palmbeach192';
				$dbname = 'data';
				$conn = new mysqli($servername, $username, $password, $dbname);

				// Get average temperature for each day.

				if ($conn->connect_error) {
					die("Connection failed: " . $conn->connect_error);
				}
				$sql = "";

				for($i = 0; $i < 24; $i++) {
					// Add a leading zero if needed.
					$iterator = sprintf('%02d', $i);
					if($i < 23) {
						$sql .= "select avg(temperature), cast(date as date) from data where date like \"2016-04-" .$iterator . "%\" UNION ";
					}
					else {
						$sql .= "select avg(temperature), cast(date as date) from data where date like \"2016-04-" .$iterator . "%\"";
					}
				}

				$result = $conn->query($sql);
				if ($result->num_rows > 0) {

					while($row = $result->fetch_assoc()) {
						// Add each value to the array. These arrays are used by the JS charts. Only add non-null values.
						if(isset($row["avg(temperature)"]) && $row["avg(temperature)"] !== "") {
							$avgTemperatures[] = $row["avg(temperature)"];
							$avgTemperatureDates[] = $row["cast(date as date)"];
						}
					}
				} else {
					echo "0 results";
					echo $sql;
				}
				$conn->close();

				?>

				<?php

				$servername = 'palm-beach.czexil0tgoyr.us-east-1.rds.amazonaws.com';
				$username = 'palm';
				$password = 'palmbeach192';
				$dbname = 'data';
				$conn = new mysqli($servername, $username, $password, $dbname);

				// Get average brightness for each day.

				if ($conn->connect_error) {
					die("Connection failed: " . $conn->connect_error);
				}
				$sql = "";

				for($i = 0; $i < 24; $i++) {
					// Add a leading zero if needed.
					$iterator = sprintf('%02d', $i);
					if($i < 23) {
						$sql .= "select avg(brightness), cast(date as date) from data where date like \"2016-04-" .$iterator . "%\" UNION ";
					}
					else {
						$sql .= "select avg(brightness), cast(date as date) from data where date like \"2016-04-" .$iterator . "%\"";
					}
				}

				$result = $conn->query($sql);
				if ($result->num_rows > 0) {

					while($row = $result->fetch_assoc()) {
						// Add each value to the array. These arrays are used by the JS charts. Only add non-null values.
						if(isset($row["avg(brightness)"]) && $row["avg(brightness)"] !== "") {
							$avgBrightnesses[] = $row["avg(brightness)"];
							$avgBrightnessDates[] = $row["cast(date as date)"];
						}
					}
				} else {
					echo "0 results";
					echo $sql;
				}
				$conn->close();

				// Reverse the order of the arrays because they are in wrong order.
				$temperatures = array_reverse($temperatures);
				$dates = array_reverse($dates);
				$brightnesses = array_reverse($brightnesses);

				?>

				<?php

				$servername = 'palm-beach.czexil0tgoyr.us-east-1.rds.amazonaws.com';
				$username = 'palm';
				$password = 'palmbeach192';
				$dbname = 'data';
				$conn = new mysqli($servername, $username, $password, $dbname);

				// Get average temperature for each hour.

				$dayNumber = date("d");
				$monthNumber = date("m");

				if ($conn->connect_error) {
					die("Connection failed: " . $conn->connect_error);
				}
				$sql = "";

				for($i = 0; $i < 24; $i++) {
					// Add a leading zero if needed.
					$iterator = sprintf('%02d', $i);
					if($i < 23) {
						$sql .= "select avg(temperature), cast(date as time) from data where date like \"2016-" . $monthNumber . "-" . $dayNumber . " " . $iterator . "%\" UNION ";
					}
					else {
						$sql .= "select avg(temperature), cast(date as time) from data where date like \"2016-" . $monthNumber . "-" . $dayNumber . " " . $iterator . "%\"";
					}
				}

				$result = $conn->query($sql);
				if ($result->num_rows > 0) {

					while($row = $result->fetch_assoc()) {
						// Add each value to the array. These arrays are used by the JS charts. Only add non-null values.
						if(isset($row["avg(temperature)"]) && $row["avg(temperature)"] !== "") {
							$avgHourlyTemperatures[] = $row["avg(temperature)"];
							$avgHourlyTemperatureDates[] = $row["cast(date as time)"];
						}
					}
				} else {
					echo "0 results";
					echo $sql;
				}
				$conn->close();

				// Reverse the order of the arrays because they are in wrong order.
				$temperatures = array_reverse($temperatures);
				$dates = array_reverse($dates);
				$brightnesses = array_reverse($brightnesses);

				?>

			</div>
		</div>
		<div class="row">
			<div class="large-6 columns">
				<div>
					<p><strong>Temperature History</strong></p>
					<canvas id="temperature-canvas"></canvas>
				</div>
			</div>
			<div class="large-6 columns">
				<div>
					<p><strong>Brightness History</strong></p>
					<canvas id="brightness-canvas"></canvas>
				</div>
			</div>
		</div>
		<div class="row">
			<div class="large-6 columns">
				<div>
					<p><strong>Daily Temperature History</strong></p>
					<canvas id="avg-temperature-canvas"></canvas>
				</div>
			</div>
			<div class="large-6 columns">
				<div>
					<p><strong>Daily Brightness History</strong></p>
					<canvas id="avg-brightness-canvas"></canvas>
				</div>
			</div>
		</div>
		<div class="row">
			<div class="large-12 columns">
				<div>
					<p><strong>Hourly Temperature History</strong></p>
					<canvas id="avg-hourly-temperature-canvas"></canvas>
				</div>
			</div>
		</div>
	</div>

<script src="https://cdn.jsdelivr.net/foundation/6.2.1/foundation.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/1.1.1/Chart.min.js"></script>
<script>
	var dates = [];
	var temperatures = [];
	var brightnesses = [];
	var avgTemperatures = [];
	var avgTemperatureDates = [];
	var avgHourlyTemperatures = [];
	var avgHourlyTemperatureDates = [];
	var avgBrightnesses = [];
	var avgBrightnessDates = [];
	var avgHourlyBrightnesses = [];
	var avgHourlyBrightnessDates = [];

	<?php
		foreach($dates as $date) {
			echo 'dates.push("' . $date . '");';
		}
		foreach($temperatures as $temperature) {
			echo 'temperatures.push("' . $temperature . '");';
		}
		foreach($brightnesses as $brightness) {
			echo 'brightnesses.push("' . $brightness . '");';
		}
		foreach($avgTemperatures as $avgTemperature) {
			echo 'avgTemperatures.push("' . $avgTemperature . '");';
		}
		foreach($avgTemperatureDates as $avgTemperatureDate) {
			echo 'avgTemperatureDates.push("' . $avgTemperatureDate . '");';
		}
		foreach($avgBrightnesses as $avgBrightness) {
			echo 'avgBrightnesses.push("' . $avgBrightness . '");';
		}
		foreach($avgBrightnessDates as $avgBrightnessDate) {
			echo 'avgBrightnessDates.push("' . $avgBrightnessDate . '");';
		}
		foreach($avgHourlyTemperatures as $avgHourlyTemperature) {
			echo 'avgHourlyTemperatures.push("' . $avgHourlyTemperature . '");';
		}
		foreach($avgHourlyTemperatureDates as $avgHourlyTemperatureDate) {
			echo 'avgHourlyTemperatureDates.push("' . $avgHourlyTemperatureDate . '");';
		}
	?>

	Chart.defaults.global.animation = false;

	var temperatureChartData = {
		labels : dates,
		datasets : [
			{
				label: "Temperature History",
				fillColor : "transparent",
				strokeColor : "rgba(61,166,82,1)",
				pointColor : "rgba(0,0,0,1)",
				pointStrokeColor : "#fff",
				pointHighlightFill : "#fff",
				pointHighlightStroke : "rgba(220,220,220,1)",
				data : temperatures,
				scaleOverride: true,
				scaleSteps: 10,
				scaleStepsWidth: 1
			}
		]
	};
	var avgTemperatureChartData = {
		labels : avgTemperatureDates,
		datasets : [
			{
				label: "Average Temperature History",
				fillColor : "transparent",
				strokeColor : "rgba(61,166,82,1)",
				pointColor : "rgba(0,0,0,1)",
				pointStrokeColor : "#fff",
				pointHighlightFill : "#fff",
				pointHighlightStroke : "rgba(220,220,220,1)",
				data : avgTemperatures,
				scaleOverride: true,
				scaleSteps: 10,
				scaleStepsWidth: 1
			}
		]
	};
	var avgHourlyTemperatureChartData = {
		labels : avgHourlyTemperatureDates,
		datasets : [
			{
				label: "Hourly Temperature History",
				fillColor : "transparent",
				strokeColor : "rgba(61,166,82,1)",
				pointColor : "rgba(0,0,0,1)",
				pointStrokeColor : "#fff",
				pointHighlightFill : "#fff",
				pointHighlightStroke : "rgba(220,220,220,1)",
				data : avgHourlyTemperatures,
				scaleOverride: true,
				scaleSteps: 10,
				scaleStepsWidth: 1
			}
		]
	};
	var brightnessChartData = {
		labels : dates,
		datasets : [
			{
				label: "Brightness History",
				fillColor : "transparent",
				strokeColor : "rgba(61,166,82,1)",
				pointColor : "rgba(0,0,0,1)",
				pointStrokeColor : "#fff",
				pointHighlightFill : "#fff",
				pointHighlightStroke : "rgba(220,220,220,1)",
				data : brightnesses,
				scaleOverride: true,
				scaleSteps: 10,
				scaleStepsWidth: 1
			}
		]
	};
	var avgBrightnessChartData = {
		labels : avgBrightnessDates,
		datasets : [
			{
				label: "Brightness History",
				fillColor : "transparent",
				strokeColor : "rgba(61,166,82,1)",
				pointColor : "rgba(0,0,0,1)",
				pointStrokeColor : "#fff",
				pointHighlightFill : "#fff",
				pointHighlightStroke : "rgba(220,220,220,1)",
				data : avgBrightnesses,
				scaleOverride: true,
				scaleSteps: 10,
				scaleStepsWidth: 1
			}
		]
	};
	window.onload = function(){
		var temperatureChartContext = document.getElementById("temperature-canvas").getContext("2d");
		window.myLine = new Chart(temperatureChartContext).Line(temperatureChartData, {
			responsive: true
		});
		var brightnessChartContext = document.getElementById("brightness-canvas").getContext("2d");
		window.myLine2 = new Chart(brightnessChartContext).Line(brightnessChartData, {
			responsive: true
		});
		var avgTemperatureChartContext = document.getElementById("avg-temperature-canvas").getContext("2d");
		window.myLine3 = new Chart(avgTemperatureChartContext).Line(avgTemperatureChartData, {
			responsive: true
		});
		var avgBrightnessChartContext = document.getElementById("avg-brightness-canvas").getContext("2d");
		window.myLine3 = new Chart(avgBrightnessChartContext).Line(avgBrightnessChartData, {
			responsive: true
		});
		var avgHourlyTemperatureChartContext = document.getElementById("avg-hourly-temperature-canvas").getContext("2d");
		window.myLine3 = new Chart(avgHourlyTemperatureChartContext).Line(avgHourlyTemperatureChartData, {
			responsive: true
		});

		if(avgHourlyTemperatureDates.length <= 0) {
			document.getElementById("avg-hourly-temperature-canvas").innerHTML = "<p>No temperature data available for the last 24 hours.<p>";
		}
	};
</script>
</body>
</html>