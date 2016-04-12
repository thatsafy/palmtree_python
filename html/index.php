<!DOCTYPE = html>
<html>
	<head>
		<meta http-equiv="refresh" content="10">
		<style>
		
			table {
				padding: 0px;
				border-collapse: collapse;
			}
			
			th {
				padding-left: 10px;
				padding-right: 10px;
			}
			
			tr {
				height: 1.5em;
			}
			
			tr:nth-child(odd) {
				background-color: #CCC;
			}
			nav { 
				width: 100%;
			}
			nav ul {
				list-style: none;
			}
			nav ul li {   
				float: left;   
				display: block;   
				margin-right: 50px;   
				width: 100px;   
			}
			section { 
				float: left;
				width: 100%; 
			}
			article {
				float:left;
				clear:left;
				width: 50%;
				height: 50px;
			}
			aside { 
				float: right; 
				width: 50%;
				height: 100px;
			}
			footer { 
				clear:both; 
				background-color: #ffc;
			}


		</style>
	</head>

	<body>
		<nav>
		</nav>
		<section>
		<aside>
				<h1> LOGIN DATA </h1>
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
						
							echo "<table><tr><th>ID</th><th>Name</th><th>Time</th></tr>";
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
			</aside>
			<article>
				<h1> DATALOGS </h1>
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
					
					echo "<table><tr><th>ID</th><th>Temperature</th><th>Brightness</th><th>Date</th></tr>";
					 
					 while($row = $result->fetch_assoc()) {
						 echo "<tr><td>" . $row["id"]. "</td><td>" . $row["temperature"]. "</td><td>" . $row["brightness"]. "</td><td>" . $row["date"]. "</td></tr>";
					 }
					 echo "</table>";
				} else {
					echo "0 results";
				}
				$conn->close();
				?>
			</article>
			
		</section>
		<footer>
		</footer>
	</body>
</html>