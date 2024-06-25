// const commentLabel = document.querySelector(".comment-label");
// const commentField = document.querySelector(".comment-toggle");

// commentLabel.addEventListener("click", function() {
//     if (commentField.style.display === "none") {
//         commentField.style.display = "block";
//     } else {
//         commentField.style.display = "none";
//     }
// });


const commentLabels = document.querySelectorAll(".comment-label");
const commentFields = document.querySelectorAll(".comment-toggle");

commentLabels.forEach((label, index) => {
    label.addEventListener("click", function() {
        const commentField = commentFields[index];
        if (commentField.style.display === "none" || commentField.style.display === "") {
            commentField.style.display = "block";
        } else {
            commentField.style.display = "none";
        }
    });
});
