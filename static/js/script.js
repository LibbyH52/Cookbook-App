      $(document).ready(function(){
          $(".navbar-nav").click(function() {
              $(".navbar-collapse").collapse("toggle")
          });
          $(".new-input-btn").on('click', function(){
            $('<input type="text" class="form-control" name="ingredient" id="ingredient" placeholder="20g plain flour sieved" required >').insertBefore(".new-input-btn");
          });
          $(".remove-input-btn").on('click', function(){
              $('#ingredients-row input:last').remove();
          });
          $(".new-recipe").submit(function(){
              alert("Thank you! Your recipe has been added.");
          });
          $(".edit-recipe").submit(function(){
              alert("Thank you! This recipe has now been updated.");
          });
         /*$('.btn-filter').prop("disabled", true);*/
            
     });