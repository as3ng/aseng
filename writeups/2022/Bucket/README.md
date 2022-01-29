# Bucket
This is a quick walktrhough of cloud forensics challenge from [Cyberdefenders](https://cyberdefenders.org/blueteam-ctf-challenges/84). We're give the
credentials to access the AWS console as an Indetity and Access Management (IAM) Security account.
**Kudos** to Scott Piper and Cyberdefenders Team to provide this awesome challenge!

<img src="images/Picture1.png" />

The given scenario:

`Welcome, Defender! As an incident responder, we're granting you access to the AWS account called "Security" as an IAM user. This account contains a copy of the logs during the time period of the incident and has the ability to assume the "Security" role in the target account so you can look around to spot the misconfigurations that allowed for this attack to happen.`

Credentials:

- Login: https://flaws2-security.signin.aws.amazon.com/console
- Account ID: 3220******
- Username: ******
- Password: ******
- Access Key: AKIAIUFNQ***********
- Secret Key: ************\zUMvK4CcdXO2T7sePX0ddF

<img src="images/environ.jpg" />

# Preliminary
We'll use the following tools that can ease the investigation:
- [AWS-CLI](https://aws.amazon.com/id/cli/)

This tool is really necessary to connect to your AWS or doing some filters or gathering information from 
AWS source.
- [jq](https://stedolan.github.io/jq/)

This tool will help you to process JSON data and do some filters to ease carving the information specifically.

# Challenges

## 1. What is the full AWS CLI command used to configure credentials?

First, we'll have to visit the login page and use the given credentials. The layout interface of the homepage
shall be like this.
<img src="images/Picture2.png" />

Note that there's a region options that you may select. I'll use `us-east-1` for the default region.

<img src="images/Picture3.png" />

After you've logged in, you'll need to configure the `aws-cli` tools to be logged in as
IAM Security account using the `Access Key` and `Secret Key`.

<img src="images/Picture4.png" />

The command the we can use to configure up our credentials is `aws configure`.
The default format that I use is `JSON` since we're going to deal with `jq` tools to parse the data easily, and
choose your default region in the AWS console.

## 2. What is the 'creation' date of the bucket 'flaws2-logs'? (in UTC+00:00)

Using `aws-cli`, we can use command `aws s3api list-buckets`
```bash
aws s3api list-buckets
{
    "Buckets": [
        {
            "Name": "flaws2-logs",
            "CreationDate": "2018-11-19T20:54:31+00:00"
        }
    ],
    "Owner": {
        "DisplayName": "scott+flaws2_security",
        "ID": "0ff467deaf461e549934997a2df02d29c8010173b1464262782d522bce63bf46"
    }
}
```
The creation date is `2018-11-19 20:54:31`.
There's also alternative command using `aws s3 ls`. Yet since my default timezone is UTC+07:00, I
need to revert back 7 hours of the timeline results.

```bash
aws s3 ls             
2018-11-20 03:54:31 flaws2-logs
```
If you want to know more about the s3 Buckets, AWS documentation has covered your answers [here](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html)!

## 3. What is the name of the first generated event -according to time?

We're know proceeding to use `jq` tools. First, we need to download all the log artifacts from the buckets
to our local directory. We can use `sync` command to do it.

```bash
aws s3 sync s3://flaws2-logs /home/kali/Desktop/CTF/Cyberdefenders/AWS 
download: s3://flaws2-logs/AWSLogs/653711331788/CloudTrail/us-east-1/2018/11/28/653711331788_CloudTrail_us-east-1_20181128T2305Z_83VTWZ8Z0kiEC7Lq.json.gz to AWSLogs/653711331788/CloudTrail/us-east-1/2018/11/28/653711331788_CloudTrail_us-east-1_20181128T2305Z_83VTWZ8Z0kiEC7Lq.json.gz
download: s3://flaws2-logs/AWSLogs/653711331788/CloudTrail/us-east-1/2018/11/28/653711331788_CloudTrail_us-east-1_20181128T2310Z_jQajCuiobojD8I4y.json.gz to AWSLogs/653711331788/CloudTrail/us-east-1/2018/11/28/653711331788_CloudTrail_us-east-1_20181128T2310Z_jQajCuiobojD8I4y.json.gz
download: s3://flaws2-logs/AWSLogs/653711331788/CloudTrail/us-east-1/2018/11/28/653711331788_CloudTrail_us-east-1_20181128T2235Z_cR9ra7OH1rytWyXY.json.gz to AWSLogs/653711331788/CloudTrail/us-east-1/2018/11/28/653711331788_CloudTrail_us-east-1_20181128T2235Z_cR9ra7OH1rytWyXY.json.gz
download: s3://flaws2-logs/AWSLogs/653711331788/CloudTrail/us-east-1/2018/11/28/653711331788_CloudTrail_us-east-1_20181128T2310Z_rp9i9zxR2Vcpqfnz.json.gz to AWSLogs/653711331788/CloudTrail/us-east-1/2018/11/28/653711331788_CloudTrail_us-east-1_20181128T2310Z_rp9i9zxR2Vcpqfnz.json.gz
download: s3://flaws2-logs/AWSLogs/653711331788/CloudTrail/us-east-1/2018/11/28/653711331788_CloudTrail_us-east-1_20181128T2310Z_jJW5HfNtz7kOnvcP.json.gz to AWSLogs/653711331788/CloudTrail/us-east-1/2018/11/28/653711331788_CloudTrail_us-east-1_20181128T2310Z_jJW5HfNtz7kOnvcP.json.gz
download: s3://flaws2-logs/AWSLogs/653711331788/CloudTrail/us-east-1/2018/11/28/653711331788_CloudTrail_us-east-1_20181128T2310Z_7J9NEIxrjJsrlXSd.json.gz to AWSLogs/653711331788/CloudTrail/us-east-1/2018/11/28/653711331788_CloudTrail_us-east-1_20181128T2310Z_7J9NEIxrjJsrlXSd.json.gz
download: s3://flaws2-logs/AWSLogs/653711331788/CloudTrail/us-east-1/2018/11/28/653711331788_CloudTrail_us-east-1_20181128T2310Z_A1lhv3sWzzRIBFVk.json.gz to AWSLogs/653711331788/CloudTrail/us-east-1/2018/11/28/653711331788_CloudTrail_us-east-1_20181128T2310Z_A1lhv3sWzzRIBFVk.json.gz
download: s3://flaws2-logs/AWSLogs/653711331788/CloudTrail/us-east-1/2018/11/28/653711331788_CloudTrail_us-east-1_20181128T2305Z_zKlMhON7EpHala9u.json.gz to AWSLogs/653711331788/CloudTrail/us-east-1/2018/11/28/653711331788_CloudTrail_us-east-1_20181128T2305Z_zKlMhON7EpHala9u.json.gz
```

Later on, we'll receive some gunzipped files. We can extract it using `gunzip -d *.gz`.
We'll be given a json logs data that are retrieved from AWS CloudTrail Logs. If we open i=up one of the log, it'll consist of a one form JSON data with its child and value.

```bash
cat 653711331788_CloudTrail_us-east-1_20181128T2235Z_cR9ra7OH1rytWyXY.json
{"Records":[{"eventVersion":"1.05","userIdentity":{"type":"AWSService","invokedBy":"ecs-tasks.amazonaws.com"},"eventTime":"2018-11-28T22:31:59Z","eventSource":"sts.amazonaws.com","eventName":"AssumeRole","awsRegion":"us-east-1","sourceIPAddress":"ecs-tasks.amazonaws.com","userAgent":"ecs-tasks.amazonaws.com","requestParameters":{"roleSessionName":"d190d14a-2404-45d6-9113-4eda22d7f2c7","roleArn":"arn:aws:iam::653711331788:role/level3"},"responseElements":{"credentials":{"sessionToken":"FQoGZXIvYXdzEFAaDEbnJXLefTT+kjlmKSKSBNgEUj8tJVL+szjaH5q2npYc2FIPgrLmfkRjK9KqtSW7+lo4WxteBTd77aeAcmIip4GceNBbU86zxGgS1IdNBzEOLnDw6biAzijG0Du/Qazx136qjy+kahHxPlR36C4y/0QrCUZpTFmP3uELsRIKkvhGvuBr6S10pTOZ+GjtUXN3iFV8Ea0KOo/fSP0d4LbZGwI957aJxs2I7N8ji/lKTfwPdq+sxXvSWnaOseinUxZUDS0zdI69CKb6C+qwhR5YTifqyuOvC9OoSlfcBN2FyHpRZf5Bd+Z+mPYTldbAvD/HcdbQo7U4jqlR2WGuXoBfwvypt/Kb6HtPp4g9O0HlTCc7Sb4uiJY81WMbaNFmmYXyj62gi+BN5QaA90YhWn9cU1x9gqt0uEgvSk/RdrwtulTtNyJcuuFvhlD1gaJHGc4eCoWApr+J9nrbPTvSo00sc8IYIVvwOi3NRsmP+ZA9aQOV/qg2L1cYxScQrQ/pKVOnYWJ4XuB0WL8gRYdo1bGI6LWGAtOV+fzVoXU0SfWH7UmPcvttqkWsv1Rr50pspmJneXeY6Ge1szNsvyHqmPFJj7GAXnEKl9xthHK3IaDc6HEprFqYw8SyQqYWGdpeism2S+V4XpIMbQJlC06BxyOg94H0Fiffzs8wwnCUpBU0s69X2tN8sxb4U3FqKl28mwCOuuaweZeGWq5MWxU7Fop2dmjaKN+u/N8F","accessKeyId":"ASIAZQNB3KHGNXWXBSJS","expiration":"Nov 29, 2018 4:31:59 AM"}},"requestID":"6b7d6c60-f35d-11e8-becc-39e7d43d4afe","eventID":"6177ca7e-860e-482c-bde9-50c735af58d6","resources":[{"ARN":"arn:aws:iam::653711331788:role/level3","accountId":"653711331788","type":"AWS::IAM::Role"}],"eventType":"AwsApiCall","recipientAccountId":"653711331788","sharedEventID":"1d18bf74-8392-4496-9dc4-a45cb799b8b4"},{"eventVersion":"1.05","userIdentity":{"type":"AWSService","invokedBy":"ecs-tasks.amazonaws.com"},"eventTime":"2018-11-28T22:31:59Z","eventSource":"sts.amazonaws.com","eventName":"AssumeRole","awsRegion":"us-east-1","sourceIPAddress":"ecs-tasks.amazonaws.com","userAgent":"ecs-tasks.amazonaws.com","requestParameters":{"roleSessionName":"d190d14a-2404-45d6-9113-4eda22d7f2c7","roleArn":"arn:aws:iam::653711331788:role/ecsTaskExecutionRole"},"responseElements":{"credentials":{"sessionToken":"FQoGZXIvYXdzEFAaDAhihig4wSQxSSiMjSKSBOW1B0tXzW8SIP7MtRZEikuZamVqb7hEQtmgX5LDeDzpOxpP4G9U8r3cZK74HNErY8W+Scri3Y8NVr/VO7MyzIXnpXiEDo10JfNYnA+urhxB+rYtPF6o8uzm40w/lqdq1/DyOkYYuFRtqWfS4Jy1t83KYAFTuX5IkTGekMidOkIcdnHjsZKQSqKs4U3MQ4doUG4nCyEERDv9yckTPq/R4fKEPTF1BN0jycyiSiR3OTPAWaLGMGxHthAKSA5IXosrPBAq0yD2HhSKZc0kbskCZyGOQCcmVAQK4IdEjyk4Lytc+PEDasvWiGoCQPEqlwwqFJm7EPm838MjCTi4ojN9nVYRP9hFYkXdvnVG6ScwoBfbg135vN1bqYgEKDncW780xUBRYwElM4Q2/6zv7DMj0UegbRJmAwtys4phLrItQqNLWPmBbW/pNgMYoT1IKfzDmuc27AyTHtL8t25hkYOLWZG19EYKm+XeHU9gbs0aDTPssjBFPZp7ssR35IHhgcw5m+etXSoXMxMuHNbVR46ZJ6uieR8roEZ8QfiIijyB8J7i2sH2JOY0HIOonbVYmqdtv++0D+1idTO+6ZbXJIKhEmDmZZDeenF2ZXQGH4PgA4udIdBXnhVLzVFkEKc1MWG3aAhuOhZLvnXkOpkn1XjwfDx3N0UyenOUR4x/gkY9+MEXMZAyO8Va2Y1vNZvnSCvTJtHDKN+u/N8F","accessKeyId":"ASIAZQNB3KHGMG7YRUEW","expiration":"Nov 29, 2018 4:31:59 AM"}},"requestID":"6b80a0b1-f35d-11e8-becc-39e7d43d4afe","eventID":"457af3a9-0b1b-44ca-91e1-8f4a0f873149","resources":[{"ARN":"arn:aws:iam::653711331788:role/ecsTaskExecutionRole","accountId":"653711331788","type":"AWS::IAM::Role"}],"eventType":"AwsApiCall","recipientAccountId":"653711331788","sharedEventID":"5397e1a9-82c7-4a00-9b1c-e44cbd688aa1"}]}
```

Now we'll open the file again and pass it to `jq` tools to parse the JSON into more readable format.

```bash
cat 653711331788_CloudTrail_us-east-1_20181128T2235Z_cR9ra7OH1rytWyXY.json | jq
{
  "Records": [
    {
      "eventVersion": "1.05",
      "userIdentity": {
        "type": "AWSService",
        "invokedBy": "ecs-tasks.amazonaws.com"
      },
      "eventTime": "2018-11-28T22:31:59Z",
      "eventSource": "sts.amazonaws.com",
      "eventName": "AssumeRole",
      "awsRegion": "us-east-1",
      "sourceIPAddress": "ecs-tasks.amazonaws.com",
      "userAgent": "ecs-tasks.amazonaws.com",
      "requestParameters": {
        "roleSessionName": "d190d14a-2404-45d6-9113-4eda22d7f2c7",
        "roleArn": "arn:aws:iam::653711331788:role/level3"
      },
      "responseElements": {
        "credentials": {
          "sessionToken": "FQoGZXIvYXdzEFAaDEbnJXLefTT+kjlmKSKSBNgEUj8tJVL+szjaH5q2npYc2FIPgrLmfkRjK9KqtSW7+lo4WxteBTd77aeAcmIip4GceNBbU86zxGgS1IdNBzEOLnDw6biAzijG0Du/Qazx136qjy+kahHxPlR36C4y/0QrCUZpTFmP3uELsRIKkvhGvuBr6S10pTOZ+GjtUXN3iFV8Ea0KOo/fSP0d4LbZGwI957aJxs2I7N8ji/lKTfwPdq+sxXvSWnaOseinUxZUDS0zdI69CKb6C+qwhR5YTifqyuOvC9OoSlfcBN2FyHpRZf5Bd+Z+mPYTldbAvD/HcdbQo7U4jqlR2WGuXoBfwvypt/Kb6HtPp4g9O0HlTCc7Sb4uiJY81WMbaNFmmYXyj62gi+BN5QaA90YhWn9cU1x9gqt0uEgvSk/RdrwtulTtNyJcuuFvhlD1gaJHGc4eCoWApr+J9nrbPTvSo00sc8IYIVvwOi3NRsmP+ZA9aQOV/qg2L1cYxScQrQ/pKVOnYWJ4XuB0WL8gRYdo1bGI6LWGAtOV+fzVoXU0SfWH7UmPcvttqkWsv1Rr50pspmJneXeY6Ge1szNsvyHqmPFJj7GAXnEKl9xthHK3IaDc6HEprFqYw8SyQqYWGdpeism2S+V4XpIMbQJlC06BxyOg94H0Fiffzs8wwnCUpBU0s69X2tN8sxb4U3FqKl28mwCOuuaweZeGWq5MWxU7Fop2dmjaKN+u/N8F",                                                                                                                                                                   
          "accessKeyId": "ASIAZQNB3KHGNXWXBSJS",
          "expiration": "Nov 29, 2018 4:31:59 AM"
        }
      },
      "requestID": "6b7d6c60-f35d-11e8-becc-39e7d43d4afe",
      "eventID": "6177ca7e-860e-482c-bde9-50c735af58d6",
      "resources": [
        {
          "ARN": "arn:aws:iam::653711331788:role/level3",
          "accountId": "653711331788",
          "type": "AWS::IAM::Role"
        }
      ],
      "eventType": "AwsApiCall",
      "recipientAccountId": "653711331788",
      "sharedEventID": "1d18bf74-8392-4496-9dc4-a45cb799b8b4"
    },
    {
      "eventVersion": "1.05",
      "userIdentity": {
        "type": "AWSService",
        "invokedBy": "ecs-tasks.amazonaws.com"
      },
      "eventTime": "2018-11-28T22:31:59Z",
      "eventSource": "sts.amazonaws.com",
      "eventName": "AssumeRole",
      "awsRegion": "us-east-1",
      "sourceIPAddress": "ecs-tasks.amazonaws.com",
      "userAgent": "ecs-tasks.amazonaws.com",
      "requestParameters": {
        "roleSessionName": "d190d14a-2404-45d6-9113-4eda22d7f2c7",
        "roleArn": "arn:aws:iam::653711331788:role/ecsTaskExecutionRole"
      },
      "responseElements": {
        "credentials": {
          "sessionToken": "FQoGZXIvYXdzEFAaDAhihig4wSQxSSiMjSKSBOW1B0tXzW8SIP7MtRZEikuZamVqb7hEQtmgX5LDeDzpOxpP4G9U8r3cZK74HNErY8W+Scri3Y8NVr/VO7MyzIXnpXiEDo10JfNYnA+urhxB+rYtPF6o8uzm40w/lqdq1/DyOkYYuFRtqWfS4Jy1t83KYAFTuX5IkTGekMidOkIcdnHjsZKQSqKs4U3MQ4doUG4nCyEERDv9yckTPq/R4fKEPTF1BN0jycyiSiR3OTPAWaLGMGxHthAKSA5IXosrPBAq0yD2HhSKZc0kbskCZyGOQCcmVAQK4IdEjyk4Lytc+PEDasvWiGoCQPEqlwwqFJm7EPm838MjCTi4ojN9nVYRP9hFYkXdvnVG6ScwoBfbg135vN1bqYgEKDncW780xUBRYwElM4Q2/6zv7DMj0UegbRJmAwtys4phLrItQqNLWPmBbW/pNgMYoT1IKfzDmuc27AyTHtL8t25hkYOLWZG19EYKm+XeHU9gbs0aDTPssjBFPZp7ssR35IHhgcw5m+etXSoXMxMuHNbVR46ZJ6uieR8roEZ8QfiIijyB8J7i2sH2JOY0HIOonbVYmqdtv++0D+1idTO+6ZbXJIKhEmDmZZDeenF2ZXQGH4PgA4udIdBXnhVLzVFkEKc1MWG3aAhuOhZLvnXkOpkn1XjwfDx3N0UyenOUR4x/gkY9+MEXMZAyO8Va2Y1vNZvnSCvTJtHDKN+u/N8F",                                                                                                                                                                   
          "accessKeyId": "ASIAZQNB3KHGMG7YRUEW",
          "expiration": "Nov 29, 2018 4:31:59 AM"
        }
      },
      "requestID": "6b80a0b1-f35d-11e8-becc-39e7d43d4afe",
      "eventID": "457af3a9-0b1b-44ca-91e1-8f4a0f873149",
      "resources": [
        {
          "ARN": "arn:aws:iam::653711331788:role/ecsTaskExecutionRole",
          "accountId": "653711331788",
          "type": "AWS::IAM::Role"
        }
      ],
      "eventType": "AwsApiCall",
      "recipientAccountId": "653711331788",
      "sharedEventID": "5397e1a9-82c7-4a00-9b1c-e44cbd688aa1"
    }
  ]
}
```

It is now more structured right? We want to get the first event generated, so we'll pay attention on
the time which located in `eventTime` and the `eventName` for the answer. 
We'll use the `jq` tools to filter out and results the satisfying conditions. Since the `Records` is the parent-array,
we'll define it and pipe the required child parameter.

```bash
cat *.json | jq -r ".Records[]|{eventTime,eventName}"
{
  "eventTime": "2018-11-28T22:31:59Z",
  "eventName": "AssumeRole"
}
{
  "eventTime": "2018-11-28T22:31:59Z",
  "eventName": "AssumeRole"
}
{
  "eventTime": "2018-11-28T23:03:12Z",
  "eventName": "CreateLogStream"
}
{
  "eventTime": "2018-11-28T23:02:56Z",
  "eventName": "GetObject"
}
{
  "eventTime": "2018-11-28T23:03:08Z",
  "eventName": "GetObject"
}
{
  "eventTime": "2018-11-28T23:03:11Z",
  "eventName": "GetObject"
}
{
  "eventTime": "2018-11-28T23:03:20Z",
  "eventName": "Invoke"
}
{
  "eventTime": "2018-11-28T23:03:50Z",
  "eventName": "CreateLogStream"
}
{
  "eventTime": "2018-11-28T23:03:12Z",
  "eventName": "AssumeRole"
}
{
  "eventTime": "2018-11-28T23:03:20Z",
  "eventName": "CreateLogStream"
}
{
  "eventTime": "2018-11-28T23:03:13Z",
  "eventName": "CreateLogStream"
}
{
  "eventTime": "2018-11-28T23:05:53Z",
  "eventName": "ListImages"
}
{
  "eventTime": "2018-11-28T23:03:35Z",
  "eventName": "CreateLogStream"
}
{
  "eventTime": "2018-11-28T23:06:17Z",
  "eventName": "BatchGetImage"
}
{
  "eventTime": "2018-11-28T23:06:33Z",
  "eventName": "GetDownloadUrlForLayer"
}
{
  "eventTime": "2018-11-28T23:02:56Z",
  "eventName": "GetObject"
}
{
  "eventTime": "2018-11-28T23:02:56Z",
  "eventName": "GetObject"
}
{
  "eventTime": "2018-11-28T23:02:56Z",
  "eventName": "GetObject"
}
{
  "eventTime": "2018-11-28T23:02:57Z",
  "eventName": "GetObject"
}
{
  "eventTime": "2018-11-28T23:03:08Z",
  "eventName": "GetObject"
}
{
  "eventTime": "2018-11-28T23:03:08Z",
  "eventName": "GetObject"
}
{
  "eventTime": "2018-11-28T23:03:08Z",
  "eventName": "GetObject"
}
{
  "eventTime": "2018-11-28T23:03:08Z",
  "eventName": "GetObject"
}
{
  "eventTime": "2018-11-28T23:03:11Z",
  "eventName": "GetObject"
}
{
  "eventTime": "2018-11-28T23:03:13Z",
  "eventName": "Invoke"
}
{
  "eventTime": "2018-11-28T23:03:14Z",
  "eventName": "GetObject"
}
{
  "eventTime": "2018-11-28T23:03:17Z",
  "eventName": "GetObject"
}
{
  "eventTime": "2018-11-28T23:03:18Z",
  "eventName": "GetObject"
}
{
  "eventTime": "2018-11-28T23:04:54Z",
  "eventName": "ListObjects"
}
{
  "eventTime": "2018-11-28T23:05:10Z",
  "eventName": "GetObject"
}
{
  "eventTime": "2018-11-28T23:05:12Z",
  "eventName": "GetObject"
}
{
  "eventTime": "2018-11-28T23:05:12Z",
  "eventName": "GetObject"
}
{
  "eventTime": "2018-11-28T23:07:08Z",
  "eventName": "GetObject"
}
{
  "eventTime": "2018-11-28T23:07:08Z",
  "eventName": "GetObject"
}
{
  "eventTime": "2018-11-28T23:09:28Z",
  "eventName": "ListBuckets"
}
{
  "eventTime": "2018-11-28T23:09:36Z",
  "eventName": "GetObject"
}
{
  "eventTime": "2018-11-28T23:09:36Z",
  "eventName": "GetObject"
}
```

As we can see, the first generated event (on the result above) is `AssumeRole`.

## 4. What source IP address generated the event dated 2018-11-28 at 23:03:20 UTC?

Note that the `eventTime` has `T` and `Z` in the JSON format, we'll want to filter out the result
accourding to the eventTime that **equals** to `2018-11-28T23:03:20Z`.

```bash
cat * | jq -r '.Records[] | select(.eventTime == "2018-11-28T23:03:20Z") | .sourceIPAddress'
apigateway.amazonaws.com
34.234.236.212
```

The IP Address is `34.234.236.212`.

## 5. Which IP address does not belong to Amazon AWS infrastructure?

If we take a look at the logs, note that only 2 IP Address that are assigned there. There's a **user-agent** 
value which we can count on to determine whether it was accessed from `aws` or not.
Therefore, we can filter it using this command.

```bash
cat * | jq -r '.Records[] | {eventSource,sourceIPAddress,userAgent}'
{
  "eventSource": "sts.amazonaws.com",
  "sourceIPAddress": "ecs-tasks.amazonaws.com",
  "userAgent": "ecs-tasks.amazonaws.com"
}
{
  "eventSource": "sts.amazonaws.com",
  "sourceIPAddress": "ecs-tasks.amazonaws.com",
  "userAgent": "ecs-tasks.amazonaws.com"
}
{
  "eventSource": "logs.amazonaws.com",
  "sourceIPAddress": "34.234.236.212",
  "userAgent": "awslambda-worker"
}
{
  "eventSource": "s3.amazonaws.com",
  "sourceIPAddress": "104.102.221.250",
  "userAgent": "[Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36]"
}
{
  "eventSource": "s3.amazonaws.com",
  "sourceIPAddress": "104.102.221.250",
  "userAgent": "[Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36]"
}
{
  "eventSource": "s3.amazonaws.com",
  "sourceIPAddress": "104.102.221.250",
  "userAgent": "[Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36]"
}
{
  "eventSource": "lambda.amazonaws.com",
  "sourceIPAddress": "apigateway.amazonaws.com",
  "userAgent": "apigateway.amazonaws.com"
}
{
  "eventSource": "logs.amazonaws.com",
  "sourceIPAddress": "34.234.236.212",
  "userAgent": "awslambda-worker"
}
{
  "eventSource": "sts.amazonaws.com",
  "sourceIPAddress": "lambda.amazonaws.com",
  "userAgent": "lambda.amazonaws.com"
}
{
  "eventSource": "logs.amazonaws.com",
  "sourceIPAddress": "34.234.236.212",
  "userAgent": "awslambda-worker"
}
{
  "eventSource": "logs.amazonaws.com",
  "sourceIPAddress": "34.234.236.212",
  "userAgent": "awslambda-worker"
}
{
  "eventSource": "ecr.amazonaws.com",
  "sourceIPAddress": "104.102.221.250",
  "userAgent": "aws-cli/1.16.19 Python/2.7.10 Darwin/17.7.0 botocore/1.12.9"
}
{
  "eventSource": "logs.amazonaws.com",
  "sourceIPAddress": "34.234.236.212",
  "userAgent": "awslambda-worker"
}
{
  "eventSource": "ecr.amazonaws.com",
  "sourceIPAddress": "104.102.221.250",
  "userAgent": "aws-cli/1.16.19 Python/2.7.10 Darwin/17.7.0 botocore/1.12.9"
}
{
  "eventSource": "ecr.amazonaws.com",
  "sourceIPAddress": "104.102.221.250",
  "userAgent": "aws-cli/1.16.19 Python/2.7.10 Darwin/17.7.0 botocore/1.12.9"
}
{
  "eventSource": "s3.amazonaws.com",
  "sourceIPAddress": "104.102.221.250",
  "userAgent": "[Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36]"
}
{
  "eventSource": "s3.amazonaws.com",
  "sourceIPAddress": "104.102.221.250",
  "userAgent": "[Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36]"
}
{
  "eventSource": "s3.amazonaws.com",
  "sourceIPAddress": "104.102.221.250",
  "userAgent": "[Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36]"
}
{
  "eventSource": "s3.amazonaws.com",
  "sourceIPAddress": "104.102.221.250",
  "userAgent": "[Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36]"
}
{
  "eventSource": "s3.amazonaws.com",
  "sourceIPAddress": "104.102.221.250",
  "userAgent": "[Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36]"
}
{
  "eventSource": "s3.amazonaws.com",
  "sourceIPAddress": "104.102.221.250",
  "userAgent": "[Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36]"
}
{
  "eventSource": "s3.amazonaws.com",
  "sourceIPAddress": "104.102.221.250",
  "userAgent": "[Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36]"
}
{
  "eventSource": "s3.amazonaws.com",
  "sourceIPAddress": "104.102.221.250",
  "userAgent": "[Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36]"
}
{
  "eventSource": "s3.amazonaws.com",
  "sourceIPAddress": "104.102.221.250",
  "userAgent": "[Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36]"
}
{
  "eventSource": "lambda.amazonaws.com",
  "sourceIPAddress": "apigateway.amazonaws.com",
  "userAgent": "apigateway.amazonaws.com"
}
{
  "eventSource": "s3.amazonaws.com",
  "sourceIPAddress": "104.102.221.250",
  "userAgent": "[Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36]"
}
{
  "eventSource": "s3.amazonaws.com",
  "sourceIPAddress": "104.102.221.250",
  "userAgent": "[Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36]"
}
{
  "eventSource": "s3.amazonaws.com",
  "sourceIPAddress": "104.102.221.250",
  "userAgent": "[Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36]"
}
{
  "eventSource": "s3.amazonaws.com",
  "sourceIPAddress": "104.102.221.250",
  "userAgent": "[aws-cli/1.16.19 Python/2.7.10 Darwin/17.7.0 botocore/1.12.9]"
}
{
  "eventSource": "s3.amazonaws.com",
  "sourceIPAddress": "104.102.221.250",
  "userAgent": "[Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36]"
}
{
  "eventSource": "s3.amazonaws.com",
  "sourceIPAddress": "104.102.221.250",
  "userAgent": "[Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36]"
}
{
  "eventSource": "s3.amazonaws.com",
  "sourceIPAddress": "104.102.221.250",
  "userAgent": "[Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36]"
}
{
  "eventSource": "s3.amazonaws.com",
  "sourceIPAddress": "104.102.221.250",
  "userAgent": "[Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36]"
}
{
  "eventSource": "s3.amazonaws.com",
  "sourceIPAddress": "104.102.221.250",
  "userAgent": "[Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36]"
}
{
  "eventSource": "s3.amazonaws.com",
  "sourceIPAddress": "104.102.221.250",
  "userAgent": "[aws-cli/1.16.19 Python/2.7.10 Darwin/17.7.0 botocore/1.12.9]"
}
{
  "eventSource": "s3.amazonaws.com",
  "sourceIPAddress": "104.102.221.250",
  "userAgent": "[Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36]"
}
{
  "eventSource": "s3.amazonaws.com",
  "sourceIPAddress": "104.102.221.250",
  "userAgent": "[Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36]"
}
```
IP `104.102.221.250` is not derived from AWS. We'll make sure it using the `whois` command.

```bash
whois 34.234.236.212 

#
# ARIN WHOIS data and services are subject to the Terms of Use
# available at: https://www.arin.net/resources/registry/whois/tou/
#
# If you see inaccuracies in the results, please report at
# https://www.arin.net/resources/registry/whois/inaccuracy_reporting/
#
# Copyright 1997-2022, American Registry for Internet Numbers, Ltd.
#


NetRange:       34.192.0.0 - 34.255.255.255
CIDR:           34.192.0.0/10
NetName:        AT-88-Z
NetHandle:      NET-34-192-0-0-1
Parent:         NET34 (NET-34-0-0-0-0)
NetType:        Direct Allocation
OriginAS:       
Organization:   Amazon Technologies Inc. (AT-88-Z)
RegDate:        2016-09-12
Updated:        2016-09-12
Ref:            https://rdap.arin.net/registry/ip/34.192.0.0



OrgName:        Amazon Technologies Inc.
OrgId:          AT-88-Z
Address:        410 Terry Ave N.
City:           Seattle
StateProv:      WA
PostalCode:     98109
Country:        US
RegDate:        2011-12-08
Updated:        2021-07-28
Comment:        All abuse reports MUST include:
Comment:        * src IP
Comment:        * dest IP (your IP)
Comment:        * dest port
Comment:        * Accurate date/timestamp and timezone of activity
Comment:        * Intensity/frequency (short log extracts)
Comment:        * Your contact details (phone and email) Without these we will be unable to identify the correct owner of the IP address at that point in time.
Ref:            https://rdap.arin.net/registry/entity/AT-88-Z


OrgRoutingHandle: ARMP-ARIN
OrgRoutingName:   AWS RPKI Management POC
OrgRoutingPhone:  +1-206-266-4064 
OrgRoutingEmail:  aws-rpki-routing-poc@amazon.com
OrgRoutingRef:    https://rdap.arin.net/registry/entity/ARMP-ARIN

OrgNOCHandle: AANO1-ARIN
OrgNOCName:   Amazon AWS Network Operations
OrgNOCPhone:  +1-206-266-4064 
OrgNOCEmail:  amzn-noc-contact@amazon.com
OrgNOCRef:    https://rdap.arin.net/registry/entity/AANO1-ARIN

OrgTechHandle: ANO24-ARIN
OrgTechName:   Amazon EC2 Network Operations
OrgTechPhone:  +1-206-266-4064 
OrgTechEmail:  amzn-noc-contact@amazon.com
OrgTechRef:    https://rdap.arin.net/registry/entity/ANO24-ARIN

OrgRoutingHandle: IPROU3-ARIN
OrgRoutingName:   IP Routing
OrgRoutingPhone:  +1-206-266-4064 
OrgRoutingEmail:  aws-routing-poc@amazon.com
OrgRoutingRef:    https://rdap.arin.net/registry/entity/IPROU3-ARIN

OrgAbuseHandle: AEA8-ARIN
OrgAbuseName:   Amazon EC2 Abuse
OrgAbusePhone:  +1-206-266-4064 
OrgAbuseEmail:  abuse@amazonaws.com
OrgAbuseRef:    https://rdap.arin.net/registry/entity/AEA8-ARIN
```
IP `34.234.236.212` originated from Organization `Amazon`, which means it is part of AWS infrastructure, while on
the other hand:

```bash
whois 104.102.221.250

#
# ARIN WHOIS data and services are subject to the Terms of Use
# available at: https://www.arin.net/resources/registry/whois/tou/
#
# If you see inaccuracies in the results, please report at
# https://www.arin.net/resources/registry/whois/inaccuracy_reporting/
#
# Copyright 1997-2022, American Registry for Internet Numbers, Ltd.
#


NetRange:       104.64.0.0 - 104.127.255.255
CIDR:           104.64.0.0/10
NetName:        AKAMAI
NetHandle:      NET-104-64-0-0-1
Parent:         NET104 (NET-104-0-0-0-0)
NetType:        Direct Allocation
OriginAS:       
Organization:   Akamai Technologies, Inc. (AKAMAI)
RegDate:        2014-04-22
Updated:        2014-04-22
Ref:            https://rdap.arin.net/registry/ip/104.64.0.0



OrgName:        Akamai Technologies, Inc.
OrgId:          AKAMAI
Address:        145 Broadway
City:           Cambridge
StateProv:      MA
PostalCode:     02142
Country:        US
RegDate:        1999-01-21
Updated:        2021-10-12
Ref:            https://rdap.arin.net/registry/entity/AKAMAI


OrgTechHandle: SJS98-ARIN
OrgTechName:   Schecter, Steven Jay
OrgTechPhone:  +1-617-274-7134 
OrgTechEmail:  ip-admin@akamai.com
OrgTechRef:    https://rdap.arin.net/registry/entity/SJS98-ARIN

OrgAbuseHandle: NUS-ARIN
OrgAbuseName:   NOC United States
OrgAbusePhone:  +1-617-444-2535 
OrgAbuseEmail:  abuse@akamai.com
OrgAbuseRef:    https://rdap.arin.net/registry/entity/NUS-ARIN

OrgTechHandle: IPADM11-ARIN
OrgTechName:   ipadmin
OrgTechPhone:  +1-617-444-0017 
OrgTechEmail:  ip-admin@akamai.com
OrgTechRef:    https://rdap.arin.net/registry/entity/IPADM11-ARIN

OrgTechHandle: YKS-ARIN
OrgTechName:   Yeung, Kam Sze 
OrgTechPhone:  +852-22718527 
OrgTechEmail:  ip-admin@akamai.com
OrgTechRef:    https://rdap.arin.net/registry/entity/YKS-ARIN
```

IP `104.102.221.250` originated from `Akamai`, which doesn't belong to AWS Infrastructure. Therefore,
the answer is `104.102.221.250`.

## 6. Which user issued the 'ListBuckets' request?

We can filter out the logs based on the `eventName` that equals to `ListBuckets`.

```bash
cat * | jq '.Records[]|select(.eventName=="ListBuckets")'
{
  "eventVersion": "1.05",
  "userIdentity": {
    "type": "AssumedRole",
    "principalId": "AROAJQMBDNUMIKLZKMF64:d190d14a-2404-45d6-9113-4eda22d7f2c7",
    "arn": "arn:aws:sts::653711331788:assumed-role/level3/d190d14a-2404-45d6-9113-4eda22d7f2c7",
    "accountId": "653711331788",
    "accessKeyId": "ASIAZQNB3KHGNXWXBSJS",
    "sessionContext": {
      "attributes": {
        "mfaAuthenticated": "false",
        "creationDate": "2018-11-28T22:31:59Z"
      },
      "sessionIssuer": {
        "type": "Role",
        "principalId": "AROAJQMBDNUMIKLZKMF64",
        "arn": "arn:aws:iam::653711331788:role/level3",
        "accountId": "653711331788",
        "userName": "level3"
      }
    }
  },
  "eventTime": "2018-11-28T23:09:28Z",
  "eventSource": "s3.amazonaws.com",
  "eventName": "ListBuckets",
  "awsRegion": "us-east-1",
  "sourceIPAddress": "104.102.221.250",
  "userAgent": "[aws-cli/1.16.19 Python/2.7.10 Darwin/17.7.0 botocore/1.12.9]",
  "requestParameters": null,
  "responseElements": null,
  "requestID": "4698593B9338B27F",
  "eventID": "65e111a0-83ae-4ba8-9673-16291a804873",
  "eventType": "AwsApiCall",
  "recipientAccountId": "653711331788"
}
```

As we can see, the `userName` is `level3` who requests the `ListBuckets`.

## 7. What was the first request issued by the user 'level1'?

Just like before, we'll filter out the `eventTime`,`eventName`, and the userName that is located
inside the `userIdentity`.

```bash
cat * | jq -cr '.Records[]|[.eventTime, .eventName, .userIdentity.sessionContext.sessionIssuer.userName]'                                                                       
["2018-11-28T22:31:59Z","AssumeRole",null]
["2018-11-28T22:31:59Z","AssumeRole",null]
["2018-11-28T23:03:12Z","CreateLogStream","level1"]
["2018-11-28T23:02:56Z","GetObject",null]
["2018-11-28T23:03:08Z","GetObject",null]
["2018-11-28T23:03:11Z","GetObject",null]
["2018-11-28T23:03:20Z","Invoke",null]
["2018-11-28T23:03:50Z","CreateLogStream","level1"]
["2018-11-28T23:03:12Z","AssumeRole",null]
["2018-11-28T23:03:20Z","CreateLogStream","level1"]
["2018-11-28T23:03:13Z","CreateLogStream","level1"]
["2018-11-28T23:05:53Z","ListImages","level1"]
["2018-11-28T23:03:35Z","CreateLogStream","level1"]
["2018-11-28T23:06:17Z","BatchGetImage","level1"]
["2018-11-28T23:06:33Z","GetDownloadUrlForLayer","level1"]
["2018-11-28T23:02:56Z","GetObject",null]
["2018-11-28T23:02:56Z","GetObject",null]
["2018-11-28T23:02:56Z","GetObject",null]
["2018-11-28T23:02:57Z","GetObject",null]
["2018-11-28T23:03:08Z","GetObject",null]
["2018-11-28T23:03:08Z","GetObject",null]
["2018-11-28T23:03:08Z","GetObject",null]
["2018-11-28T23:03:08Z","GetObject",null]
["2018-11-28T23:03:11Z","GetObject",null]
["2018-11-28T23:03:13Z","Invoke",null]
["2018-11-28T23:03:14Z","GetObject",null]
["2018-11-28T23:03:17Z","GetObject",null]
["2018-11-28T23:03:18Z","GetObject",null]
["2018-11-28T23:04:54Z","ListObjects","level1"]
["2018-11-28T23:05:10Z","GetObject",null]
["2018-11-28T23:05:12Z","GetObject",null]
["2018-11-28T23:05:12Z","GetObject",null]
["2018-11-28T23:07:08Z","GetObject",null]
["2018-11-28T23:07:08Z","GetObject",null]
["2018-11-28T23:09:28Z","ListBuckets","level3"]
["2018-11-28T23:09:36Z","GetObject",null]
["2018-11-28T23:09:36Z","GetObject",null]
["2018-11-28T22:31:59Z","AssumeRole",null]
["2018-11-28T22:31:59Z","AssumeRole",null]
["2018-11-28T23:03:12Z","CreateLogStream","level1"]
["2018-11-28T23:02:56Z","GetObject",null]
["2018-11-28T23:03:08Z","GetObject",null]
["2018-11-28T23:03:11Z","GetObject",null]
["2018-11-28T23:03:20Z","Invoke",null]
["2018-11-28T23:03:50Z","CreateLogStream","level1"]
["2018-11-28T23:03:12Z","AssumeRole",null]
["2018-11-28T23:03:20Z","CreateLogStream","level1"]
["2018-11-28T23:03:13Z","CreateLogStream","level1"]
["2018-11-28T23:05:53Z","ListImages","level1"]
["2018-11-28T23:03:35Z","CreateLogStream","level1"]
["2018-11-28T23:06:17Z","BatchGetImage","level1"]
["2018-11-28T23:06:33Z","GetDownloadUrlForLayer","level1"]
["2018-11-28T23:02:56Z","GetObject",null]
["2018-11-28T23:02:56Z","GetObject",null]
["2018-11-28T23:02:56Z","GetObject",null]
["2018-11-28T23:02:57Z","GetObject",null]
["2018-11-28T23:03:08Z","GetObject",null]
["2018-11-28T23:03:08Z","GetObject",null]
["2018-11-28T23:03:08Z","GetObject",null]
["2018-11-28T23:03:08Z","GetObject",null]
["2018-11-28T23:03:11Z","GetObject",null]
["2018-11-28T23:03:13Z","Invoke",null]
["2018-11-28T23:03:14Z","GetObject",null]
["2018-11-28T23:03:17Z","GetObject",null]
["2018-11-28T23:03:18Z","GetObject",null]
["2018-11-28T23:04:54Z","ListObjects","level1"]
["2018-11-28T23:05:10Z","GetObject",null]
["2018-11-28T23:05:12Z","GetObject",null]
["2018-11-28T23:05:12Z","GetObject",null]
["2018-11-28T23:07:08Z","GetObject",null]
["2018-11-28T23:07:08Z","GetObject",null]
["2018-11-28T23:09:28Z","ListBuckets","level3"]
["2018-11-28T23:09:36Z","GetObject",null]
["2018-11-28T23:09:36Z","GetObject",null]
```

The first request made by `userName` of `level1` is `CreateLogStream`.

