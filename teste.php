//your api key that was emailed to you
$apikey = '611174065945670';

//your api secret that was emailed to you
$apisecret = 'Gr4R6anLFSZWuRHCRgo2kPfptE98jsJSRd6CkFT4KFCBQlCf21mv6frZwvx3omNI';

//the instagram account to check
$account = 'vinyof22';

$time = time();
$ch = curl_init();
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
$url = 'https://api.fakecheck.co/instagram/'.$account;
$auth = base64_encode(hash_hmac("sha1", $apikey.$time, $apisecret));
$headers = array(
'X-Auth: '.$auth, 
'X-Time: '.time(),
'X-Key: '.$apikey
);
curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
curl_setopt($ch, CURLOPT_URL, $url);
echo curl_exec($ch);