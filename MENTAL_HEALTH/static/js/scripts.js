
window.addEventListener('DOMContentLoaded', event => {

    // Navbar shrink function
    var navbarShrink = function () {
        const navbarCollapsible = document.body.querySelector('#mainNav');
        if (!navbarCollapsible) {
            return;
        }
        if (window.scrollY === 0) {
            navbarCollapsible.classList.remove('navbar-shrink')
        } else {
            navbarCollapsible.classList.add('navbar-shrink')
        }

    };

    // Shrink the navbar 
    navbarShrink();

    // Shrink the navbar when page is scrolled
    document.addEventListener('scroll', navbarShrink);

    // Activate Bootstrap scrollspy on the main nav element
    const mainNav = document.body.querySelector('#mainNav');
    if (mainNav) {
        new bootstrap.ScrollSpy(document.body, {
            target: '#mainNav',
            offset: 74,
        });
    };

    // Collapse responsive navbar when toggler is visible
    const navbarToggler = document.body.querySelector('.navbar-toggler');
    const responsiveNavItems = [].slice.call(
        document.querySelectorAll('#navbarResponsive .nav-link')
    );
    responsiveNavItems.map(function (responsiveNavItem) {
        responsiveNavItem.addEventListener('click', () => {
            if (window.getComputedStyle(navbarToggler).display !== 'none') {
                navbarToggler.click();
            }
        });
    });

});


// multistep form
$(document).ready(function(){
    
    var current_fs, next_fs, previous_fs; //fieldsets
    var opacity;
    
    $(".next").click(function(){
        if($(this).closest('fieldset').attr('id') == "detail"){
            var n = $(this).closest('fieldset').find('#Name').val();
            var x = $(this).closest('fieldset').find('#Email').val();  
            console.log(n, x);
            var testEmail = /^[A-Z0-9._%+-]+@([A-Z0-9-]+\.)+[A-Z]{2,4}$/i;
            if (testEmail.test(x)){  
                current_fs = $(this).parent();
                next_fs = $(this).parent().next();
        
                //Add Class Active
                $("#progressbar li").eq($("fieldset").index(next_fs)).addClass("active");
        
                //show the next fieldset
                next_fs.show(); 
                //hide the current fieldset with style
                current_fs.animate({opacity: 0}, {
                    step: function(now) {
                        // for making fielset appear animation
                        opacity = 1 - now;
    
                        current_fs.css({
                            'display': 'none',
                            'position': 'relative'
                        });
                        next_fs.css({'opacity': opacity});
                    }, 
                    duration: 600
                });
            }else{
                alert("enter name or valid gmail address");
            }
        }else{
            current_fs = $(this).parent();
            next_fs = $(this).parent().next();
        
            //Add Class Active
            $("#progressbar li").eq($("fieldset").index(next_fs)).addClass("active");
        
            //show the next fieldset
            next_fs.show(); 
            //hide the current fieldset with style
            current_fs.animate({opacity: 0}, {
                step: function(now) {
                    // for making fielset appear animation
                    opacity = 1 - now;
    
                    current_fs.css({
                        'display': 'none',
                        'position': 'relative'
                    });
                    next_fs.css({'opacity': opacity});
                }, 
                duration: 600
            });
        }
    });
    
    $(".previous").click(function(){
        
        current_fs = $(this).parent();
        previous_fs = $(this).parent().prev();
        
        //Remove class active
        $("#progressbar li").eq($("fieldset").index(current_fs)).removeClass("active");
        
        //show the previous fieldset
        previous_fs.show();
    
        //hide the current fieldset with style
        current_fs.animate({opacity: 0}, {
            step: function(now) {
                // for making fielset appear animation
                opacity = 1 - now;
    
                current_fs.css({
                    'display': 'none',
                    'position': 'relative'
                });
                previous_fs.css({'opacity': opacity});
            }, 
            duration: 600
        });
    });
    
});

var $panelsInput = $('fieldset input')

$panelsInput.click(function () {
        if($(this).closest('fieldset').find('input:checked').length >= 1) {
            $(this).closest('fieldset').find('.action-button').prop('disabled', false);  
        }
});

function toggleform(e) {
    var Id =(e.target.getAttribute('data-value'))
    let Items= ['#threeyear',  '#elevenyear', '#imageanalyse'];
    Items.map(function(item) {
        if(Id === item ) {
            $(item).addClass("active");
            $('html, body').animate({
                scrollTop: $(item).offset().top
            }, 'slow');
        }
        else {
            $(item).removeClass("active");
        }
    })
}

$(document).ready(function () {
    $('html, body').animate({
        scrollTop: $('#resultpage').offset().top
    }, 'slow');
});
