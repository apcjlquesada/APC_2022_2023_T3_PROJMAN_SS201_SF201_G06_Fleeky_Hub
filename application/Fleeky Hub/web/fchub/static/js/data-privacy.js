function data_privacy() {
    var txt;
    var message = 
    "Data Privacy Notice " +
    "We take data privacy seriously and are committed to protecting your personal information. This notice explains how we collect, use, and protect your data when you visit our website."
    + "What data do we collect? We may collect personal information such as your name, email address, postal address, and phone number when you make a purchase or sign up for our newsletter. We may also collect non-personal information such as your IP address, browser type, and operating system."
    + "How do we use your data? We may use your data to process your orders, provide customer support, send you marketing materials, and improve our website's functionality. We may also use your data to comply with legal requirements."
    + "Who do we share your data with? We may share your data with third-party service providers such as payment processors and shipping companies. We will only share the minimum amount of data necessary to provide the requested service. We may also share your data if required by law."
    + "How do we protect your data? We use appropriate technical and organizational measures to protect your data from unauthorized access, disclosure, and misuse. We limit access to your data to those who need it to provide the requested service."
    +"Your rights You have the right to access, correct, and delete your personal information. You also have the right to object to the processing of your data and to withdraw your consent at any time. To exercise these rights, please contact us at fleekycurtains@gmail.com."
    "Changes to this notice We may update this notice from time to time. Any changes will be posted on our website with the updated effective date."

    
    if (confirm(message)) {
      txt = "Loading";
    } else {
      txt = "Loading";
    }
    document.getElementById("dataprivacy").innerHTML = txt;
  }