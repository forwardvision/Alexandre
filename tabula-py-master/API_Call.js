document.getElementById("submitButton").addEventListener("click", function () {
  const dynamicInputValue = document.getElementById("dynamicInput").value;
  const pageValue = document.getElementById("page").value;
  const leftMarginValue = document.getElementById("leftMargin").value;
  const rightMarginValue = document.getElementById("rightMargin").value;
  const topMarginValue = document.getElementById("topMargin").value;
  const bottomMarginValue = document.getElementById("bottomMargin").value;
  const data = {
    pdfpathjs: dynamicInputValue,
    page: pageValue,
    leftMargin: leftMarginValue,
    rightMargin: rightMarginValue,
    topMargin: topMarginValue,
    bottomMargin: bottomMarginValue,
  };


console.log(data)
  const api_url = 'ff'

  fetch("http://127.0.0.1:5111/fetch_data", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),

    
   })
  .then((response) => {
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    // Log the response
    console.log("Raw Response:", response);

    // Return the parsed JSON response
    return response.json();
    
  })
  .then((responseData) => {
    // Log the parsed JSON response
    console.log("Raw JSON Data:", responseData.json_data);
    console.log("Data returned from Python:", responseData);
    console.log("Raw JSON Data:", responseData.json_data);  
  })
  .catch((error) => {
    // Log any errors that occurred during the request
    console.error("Error:", error);
  });
  //   .then((response) => {
  //     if (!response.ok) {
  //       throw new Error(`HTTP error! Status: ${response.status}`);
  //     }
  //     return response.json();
  //   })
  //   .then((responseData) => {
  //     console.log("Data returned from Python:", responseData);
  //   })
  //   .catch((error) => {
  //     console.error("Error:", error);
  //   });
  
});



