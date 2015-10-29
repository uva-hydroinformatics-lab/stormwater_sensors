<?php
if (isset($_POST['results']))
{
 $data = json_decode($_POST['results']);
//  This is to decode the json stream, using a function called json_decode()
	
	//scaffolding:
	// echo "data: ",gettype($data), "\n";

 // foreach($data as $record) // ACCESS each record individually
 // {
	 // echo "record: ",gettype($record), "\n";
	 // echo "*get_object_vars: ", print_r(get_object_vars($record)), "\n";
	// echo "*get_object_vars_type: ", gettype(get_object_vars($record)), "\n";
// }

$fp = fopen('raindata.csv', 'a');

//foreach ($data as $fields) {
	foreach($data as $datapoint){
		fputcsv($fp, get_object_vars($datapoint));
	}
//}

fclose($fp);
}
else
{
echo 'POST Variable not found';
}

?>
