$(function () {
    console.log("ANALYTICS");

    var merchantId = function () {
        return $('[name="merchant"]').val();
    }, beaconId = function () {
        return $('[name="beacon"]').val();
    }, dateFilter = function () {
        return {};
    }, updateStats = function (stats) {
        $('#stats').html(JSON.stringify(stats));
    };

    $('[name="merchant"]').on('change', function (event) {
        // load beacons
        // update current stats

        $.get('/analytics/' + merchantId() + '/beacons', dateFilter(), function (response) {
            var $beacons = $('[name="beacon"]');

            $beacons.html('<option value="all">All</option>');
            _.each(response.beacons, function (beacon) {
                $beacons.append($('<option>').attr('value', beacon[0]).html(beacon[1]));
            });

            updateStats(response.stats);
        }, 'json');
    });

    $('[name="beacon"]').on('change', function (event) {
        // update stats
        $.get('/analytics/' + merchantId() + '/beacons/' + beaconId(), dateFilter(), function (response) {
            updateStats(response.stats);
        }, 'json');
    });

    $('[name="time"]').on('change', function (event) {
        // update stats
    });
});
