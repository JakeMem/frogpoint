from flask import Blueprint, redirect, url_for, abort, g
from flask_login import login_required

from ..utils.decorators import render_to
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
