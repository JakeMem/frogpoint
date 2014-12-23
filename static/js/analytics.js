$(function () {
    var merchantId = function () {
        return $('[name="merchant"]').val();
    }, beaconId = function () {
        return $('[name="beacon"]').val();
    }, dateFilter = function () {
        return {};
    }, updateStats = function (stats) {
        // $('#stats-raw').html(JSON.stringify(stats));
        var $genderSplit = $('#gender-split'),
            $ageSplitMale = $('#age-split-male'),
            $ageSplitFemale = $('#age-split-female'),
            $interactions = $('#interactions');

        if (stats.gender) {
            $genderSplit.show();

            Morris.Donut({
                element: $genderSplit.find('.chart-container').get(0),
                data: _(stats.gender).map(function (val, key) {
                    return {label: key, value: val};
                }),
                colors: ['#30a1ec', '#76bdee']
            });
        } else {
            $genderSplit.hide();
        }

        stats.age = stats.age || {};

        if (stats.age.male) {
            $ageSplitMale.show();

            Morris.Donut({
                element: $ageSplitMale.find('.chart-container').get(0),
                data: _(stats.age.male).map(function (val, key) {
                    return {label: key, value: val};
                })
            });
        } else {
            $ageSplitMale.hide();
        }

        if (stats.age.female) {
            $ageSplitFemale.show();

            Morris.Donut({
                element: $ageSplitFemale.find('.chart-container').get(0),
                data: _(stats.age.female).map(function (val, key) {
                    return {label: key, value: val};
                })
            });
        } else {
            $ageSplitFemale.hide();
        }

        if (stats.interactions) {
            $interactions.show();
            $interactions.find('.chart-container').html('');

            Morris.Bar({
                element: $interactions.find('.chart-container').get(0),
                data: _(stats.interactions).map(function (val, key) {
                    return {beacon: val.alias, interactions: val.value};
                }),
                xkey: 'beacon',
                ykeys: ['interactions'],
                labels: ['Interactions'],
                barRatio: 0.4,
                xLabelMargin: 10,
                hideHover: 'auto',
                barColors: ["#3d88ba"]
            });
        } else {
            $interactions.hide();
        }
    };

    $('[name="merchant"]').on('change', function (event) {
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
        $.get('/analytics/' + merchantId() + '/beacons/' + beaconId(), dateFilter(), function (response) {
            updateStats(response.stats);
        }, 'json');
    });

    $('[name="time"]').on('change', function (event) {
        // update stats
    });

    if (typeof initStats == 'object') {
        updateStats(initStats);
    }
});
