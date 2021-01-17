let optCount = 1;
let optList = document.getElementById("options-list");

document.getElementById("options-new").addEventListener("click", (event) => {
  let newOpt = document.createElement("input");
  newOpt.type = "text";
  newOpt.placeholder = `Option ${++optCount}`;
  optList.appendChild(newOpt);
});

document
  .getElementById("question-submit")
  .addEventListener("click", (event) => {
    let questionInput = document.getElementById("question-input").value;
    let choices = [];

    for (var i = 0; i < optList.children.length; i++) {
      choices.push(optList.children[i].value);
    }

    axios.post("/polls", {
      question: questionInput,
      choices: choices,
      poll_id: "DWPUjoqG",
    });
  });
