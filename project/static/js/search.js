$(document).ready(function () {
    $('#searchButton').on('click', function () {
        var query = $('#searchInput').val();

        $.ajax({
            url: '{% url "search_view" %}',
            data: { 'query': query },
            dataType: 'json',
            success: function (data) {
                displayResults(data.results);
            }
        });
    });

    function displayResults(results) {
        var resultsContainer = $('#searchResults');
        resultsContainer.empty();

        if (results.length > 0) {
            for (var i = 0; i < results.length; i++) {
                resultsContainer.append('<p>' + results[i].your_field + '</p>');
            }
        } else {
            resultsContainer.append('<p>No results found.</p>');
        }
    }
});