$(document).ready(function() {

    $(".toggle-accordion").on("click", function() {
      var accordionId = $(this).attr("accordion-id"),
        numPanelOpen = $(accordionId + ' .collapse.in').length;
      
      $(this).toggleClass("active");
  
      if (numPanelOpen == 0) {
        closeAllPanels(accordionId);
      } else {
        openAllPanels(accordionId);
      }
    })
  
    $(".toggle-accordion2").on("click", function() {
        var accordionId = $(this).attr("accordion-id"),
          numPanelOpen = $(accordionId + ' .collapse.in').length;
        
        $(this).toggleClass("active");
    
        if (numPanelOpen == 0) {
          openAllPanels(accordionId);
        } else {
            closeAllPanels(accordionId);
        }
      })

    openAllPanels = function(aId) {
      console.log("setAllPanelclose");
      $(aId + ' .panel-collapse.in').collapse('show');
    }
    closeAllPanels = function(aId) {
        console.log("setAllPanelclose");
        $(aId + ' .panel-collapse.in').collapse('hide');
      }
  });