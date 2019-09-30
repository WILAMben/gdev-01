<?php
	
/* Email Address */	
$to      = 'support@companyname.com';

/* Subject */
$subject = 'Homeshop Newsletter Form';

/* Headers */
$headers = 'From: webmaster@example.com' . "\r\n" .
    'Reply-To: webmaster@example.com' . "\r\n" .
    'X-Mailer: PHP/' . phpversion();
	

if(isset($_POST['newsletter-email']) && !empty($_POST['newsletter-email'])){
	
	$email = $_POST['newsletter-email'];
	
	if (filter_var($email, FILTER_VALIDATE_EMAIL)) {
		
		$message = 'Email: '.$email;
		
		mail($to, $subject, $message, $headers);
		echo "Thanks for subscribing to our newsletter list.";
		
	}else{
	
		echo 'Email address is not valid';
		
	}
	
}else{

	echo 'Please, fill in all the fields';
	
}




?>