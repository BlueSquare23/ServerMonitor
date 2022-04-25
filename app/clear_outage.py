from flask import redirect, Blueprint, flash
from .models import Alert, Outage
from . import db

clear_outage_blueprint = Blueprint("clear_outage_blueprint", __name__)

# Outage blueprint decorator.
@clear_outage_blueprint.route('/<int:id>', methods=['GET'])

#@app.route('/clear_outage/<int:id>')

def clear(id):
	outage_to_clear = Outage.query.get_or_404(id)

	# Context: If you try to clear an outage that is also an active alert it
	# will just be instantly re-added to the Outage table on page refresh. So I
	# flash a message instead.

	# Checks if Alert table is populated yet.
	if Alert.query.first() != None:
		# If the chosen outage is the same as the current alert, flash message.
		alerts = Alert.query.all()
		for alert in alerts:
#		if outage_to_clear.last_logged == Alert.query.first().last_logged:
			if outage_to_clear.last_logged == alert.last_logged:
				flash('Cannot clear report about an ongoing outage!', category='error')
				return redirect('/')

	try:
		db.session.delete(outage_to_clear)
		db.session.commit()
		flash('Outage report cleared!', category='success')
		return redirect('/')
	except:
		return "Can't clear entry!"

