document.addEventListener('DOMContentLoaded', function() {
    // Find all static method elements
    var properties = document.querySelectorAll('em.property>span.pre');

    properties.forEach(function(propertyElem) {
        if (propertyElem.innerText == 'virtual')
        {
            var virtualMethodLink = document.createElement('a');
            virtualMethodLink.href = '../faq.html#what-are-virtual-methods';
            virtualMethodLink.className = 'pre virtualmethod-link';
            virtualMethodLink.innerHTML = propertyElem.innerHTML;

            // Create custom tooltip with HTML
            var tooltip = document.createElement('div');
            tooltip.className = 'custom-tooltip';
            tooltip.innerHTML = `
                <h4>Virtual Methods</h4>
                <p>In PyQGIS, <b>only</b> methods marked as 'virtual' can be safely overridden in a Python subclass of this class.</p>
                <p>Click for more details.</p>
            `;

            virtualMethodLink.appendChild(tooltip);

            propertyElem.parentNode.replaceChild(virtualMethodLink, propertyElem);

            propertyElem.classList.add("virtualmethod");
        }
    });
});
