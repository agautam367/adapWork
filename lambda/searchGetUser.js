var aws = require('aws-sdk');

var ses = new aws.SES();

exports.handler = async(event, context, callback) => {
    console.log(event);

    console.log(event.request);
    console.log(event.request.userAttributes);
    console.log(event.request.userAttributes.email);
    if (event.request.userAttributes.email) {
            sendEmail(event.request.userAttributes.email, "Congratulations " + event.userName + ", you have been confirmed: ", function(status) {

            // Return to Amazon Cognito
            callback(null, event);
        });
    } else {
        // Nothing to do, the user's email ID is unknown
        callback(null, event);
    }

    context.done(null, event);
    console.log(response);
    return {statusCode: 200,
        headers: {
            "Access-Control-Allow-Headers" : "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST"
        },
        body:event.userName
        //JSON.stringify('Hello from Lambda!')};

   // return ret;


};

function sendEmail(to, body, completedCallback) {
    console.log(to,body);
    var eParams = {
        Destination: {
            ToAddresses: [to]
        },
        Message: {
            Body: {
                Text: {
                    Data: body
                }
            },
            Subject: {
                Data: "Cognito Identity Provider registration completed"
            }
        },

        // Replace source_email with your SES validated email address
        Source: "<source_email>"
    };

    var email = ses.sendEmail(eParams, function(err, data){
        if (err) {
            console.log(err);
        } else {
            console.log("===EMAIL SENT===");
        }
        completedCallback('Email sent');
        console.log("sent");
    });
    console.log("EMAIL CODE END");
};
