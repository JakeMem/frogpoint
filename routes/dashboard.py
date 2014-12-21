from itertools import groupby

from flask import g, Blueprint, redirect, url_for, abort, jsonify
from flask_login import login_required

from ..utils.decorators import render_to, admin_required
from ..models.merchant import Merchant
from ..models.beacon import Beacon
from ..models.user_statistics import Statistic
from ..forms.beacons import AliasForm
from ..forms.coupons import CouponForm


dashboard = Blueprint('dashboard', __name__)


@dashboard.route('/')
@render_to('dashboard/home.html')
@login_required
def home():
    return redirect(url_for('dashboard.beacons'))


@dashboard.route('/beacons')
@render_to('dashboard/beacons.html')
@login_required
def beacons():
    return {
        'beacons': g.user.beacons
    }


@dashboard.route('/beacons/<beacon_id>/assign-alias', methods=('GET', 'POST'))
@render_to('dashboard/assign_alias.html')
@login_required
def assign_alias(beacon_id):
    beacon = g.user.beacon(beacon_id) or abort(404, 'Beacon not found')
    form = AliasForm(beacon)
    if form.validate_on_submit():
        form.save()
        return redirect(url_for('dashboard.beacons'))
    return {'beacon': beacon, 'form': form}


@dashboard.route('/beacons/<beacon_id>/assign-action', methods=('GET', 'POST'))
@render_to('dashboard/assign_action.html')
@login_required
def assign_action(beacon_id):
    beacon = g.user.beacon(beacon_id) or abort(404, 'Beacon not found')
    form = CouponForm(beacon)
    if form.validate_on_submit():
        form.save()
        return redirect(url_for('dashboard.beacons'))
    return {
        'beacon': beacon,
        'target_demographics': form.current_target_demographic(),
        'current_type': form.current_type(),
        'form': form
    }


@dashboard.route('/analytics', methods=('GET', 'POST'))
@render_to('dashboard/analytics.html')
@admin_required
def analytics():
    merchants = Merchant.Query.all()
    beacons = Beacon.Query.all()
    return {
        'merchants': merchants,
        'beacons': beacons,
        'stats': stats(beacons)
    }


@dashboard.route('/analytics/<merchant_id>/beacons', methods=('GET',))
@admin_required
def analytics_beacons(merchant_id):
    # Filter beacons by merchant and by date
    if merchant_id == 'all':
        beacons = Beacon.Query.all()
    else:
        beacons = Merchant.by_id(merchant_id).beacons
    return jsonify({
        'beacons': [(b.id, b.alias or b.id) for b in beacons],
        'stats': stats(beacons)
    })


@dashboard.route('/analytics/<merchant_id>/beacons/<beacon_id>',
                 methods=('GET',))
@admin_required
def analytics_beacon_stats(merchant_id, beacon_id):
    # Filter beacons by merchant and by date
    if beacon_id == 'all':
        beacons = Merchant.by_id(merchant_id).beacons
    else:
        beacons = [Beacon.by_id(beacon_id)]
    return jsonify({'stats': stats(beacons)})


def stats(beacons):
    # TODO: filter by date
    grouped = groupby(Statistic.for_beacons(beacons),
                      lambda s: s.user_gender())
    by_gender = flatten_group(grouped)
    by_age = {gender: flatten_group(groupby(items, lambda s: s.user.age_range))
                for gender, items in by_gender.items()}
    return {
        'gender': {gender: len(users) for gender, users in by_gender.items()},
        'age': {gender: {age: len(users) for age, users in values.items()}
                    for gender, values in by_age.items()}
    }


def flatten_group(group):
    return {key: list(items) for key, items in group}
