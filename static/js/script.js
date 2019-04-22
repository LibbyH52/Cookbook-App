$(document).ready(function() {
    /*Collaspes navbar when a link is clicked*/
    $(".navbar-nav").click(function() {
        $(".navbar-collapse").collapse("toggle");
    });
    /* Dynamically add new ingredient input field in recipe forms*/
    $(".new-input-btn").on("click", function() {
        $('<input type="text" class="form-control ingredient" name="ingredient" id="ingredient" placeholder="20g plain flour sieved" required >').insertBefore(".new-input-btn");
    });
    /*removes last input element in ingredient list*/
    $(".remove-input-btn").on("click", function() {
        $("#ingredients-row input:last").remove();
    });
    /*Alert popup when recipe added / edited*/
    $(".new-recipe").submit(function() {
        alert("Thank you! Your recipe has been added.");
    });
    $(".edit-recipe").submit(function() {
        alert("Thank you! This recipe has now been updated.");
    });
    /*Disable filter button if no filters selected*/
	$(".btn-filter").attr("disabled",true);
    $(".form-input").change(function() {
        $(".btn-filter").attr("disabled", $(".form-input:checked").length === 0);
   });
});