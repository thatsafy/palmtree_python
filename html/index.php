<!DOCTYPE = html>
<html>
	<head>
		<style>
			table, th, td {
				 border: 1px solid black;
			}
		</style>
	</head>

	<body>
		<?php
		$servername = 'palm-beach.czexil0tgoyr.us-east-1.rds.amazonaws.com';
		$username = 'palm';
		$password = 'palmbeach192';
		$dbname = 'data';

		$conn = new mysqli($servername, $username, $password, $dbname);
		
		if ($conn->connect_error) {
			die("Connection failed: " . $conn->connect_error);
		} 

		$sql = "SELECT id, temperature, brightness, date FROM data ORDEr BY id desc LIMIT 5";
		$result = $conn->query($sql);

		if ($result->num_rows > 0) {
			
			while($row = $result->fetch_assoc()) {
				echo "<table><tr><th>ID</th><th>Temperature</th><th>Brightness</th><th>Date</th></tr>";
				 // output data of each row
				 while($row = $result->fetch_assoc()) {
					 echo "<tr><td>" . $row["id"]. "</td><td>" . $row["temperature"]. "</td><td>" . $row["brightness"]. "</td><td>" . $row["date"]. "</td></tr>";
				 }
				 echo "</table>";
			}
		} else {
			echo "0 results";
		}
		$conn->close();
		?>
	</body>
</html>