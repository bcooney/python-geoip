from flask import Flask, request, jsonify
import pygeoip

app = Flask(__name__)

# Make sure this points to your downloaded file
gi = pygeoip.GeoIP('GeoLiteCity.dat', pygeoip.MEMORY_CACHE)

@app.route('/')
def root():
    geo_data = gi.record_by_addr(request.remote_addr)
    return jsonify(geo_data)

@app.route('/ip/<ip_address>')
def ip(ip_address):
    geo_data = gi.record_by_addr(ip_address)
    return jsonify(geo_data)

@app.route('/domain/<domain_name>')
def domain(domain_name):
    geo_data = gi.record_by_name(domain_name)
    return jsonify(geo_data)

# In general catching all 500 errors like this could be considered bad practice
# But with an app which only serves single function like ours
# It's a neat way to follow the DRY principal because all errors are the same
@app.errorhandler(500)
def error_500(e):
    return jsonify({'error': 'Error finding GeoIP data for that address'})

if __name__ == '__main__':
    app.run(port=8000, debug=False)
