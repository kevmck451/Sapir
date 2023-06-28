var activeButton = null;

function toggleFilter(buttonId) {
    var button = document.getElementById(buttonId);
    var selectedFilterInput = document.getElementById('selectedFilter');
    var selectedFilterInput_2 = document.getElementById('selectedFilter_2');

    if (button === activeButton) {
        button.classList.remove("active");
        activeButton = null;
        selectedFilterInput.value = "";  // No filter selected
        selectedFilterInput_2.value = "";
    } else {
        if (activeButton) {
            activeButton.classList.remove("active");
        }
        button.classList.add("active");
        activeButton = button;
        selectedFilterInput.value = buttonId;  // Set the selected filter
        selectedFilterInput_2.value = buttonId;
    }
}

