<?php
	
/* Email Address */	
$to      = 'support@companyname.com';

/* Headers */
$headers = 'From: webmaster@example.com' . "\r\n" .
    'Reply-To: webmaster@example.com' . "\r\n" .
    'X-Mailer: PHP/' . phpversion();


$email_message = '';

/* Errors */
$error = false;	


/* Variables */
$email = '';
$name = '';
$subject = '';
$message = '';


/* Email */
if(isset($_POST['contact-email']) && !empty($_POST['contact-email']) && $error == false){
	
	$email = $_POST['contact-email'];
	
	if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
	
		echo 'Email address is not valid';
		$error = true;
		
	}else{
		
		$headers = 'From: '. $email . "\r\n" .
					'Reply-To: '. $email . "\r\n" .
					'X-Mailer: PHP/' . phpversion();
		
	}
	
}else{

	if($error == false){
		echo 'Please, fill in all the fields';
		$error = true;
	}
	
}

/* Name */
if(isset($_POST['contact-name']) && !empty($_POST['contact-name'])){
	
	$name = $_POST['contact-name'];
	$email_message .= 'Name:' . $name . "\r\n" ;
	
}else{

	if($error == false){
		echo 'Please, fill in all the fields';
		$error = true;
	}
	
}

/* Subject */
if(isset($_POST['contact-subject']) && !empty($_POST['contact-subject'])){
	
	$subject = $_POST['contact-subject'];
	
}


/* Message */
if(isset($_POST['contact-message']) && !empty($_POST['contact-message'])){
	
	$message = $_POST['contact-message'];
	$email_message .= 'Message:' . $message . "\r\n" ;
	
}else{

	if($error == false){
		echo 'Please, fill in all the fields';
		$error = true;
	}
	
}




if($error == false){
	
	mail($to, $subject, $email_message, $headers);
	echo "Thanks for contacting us, we'll respond to you soon!";

}






?>