from flask import Blueprint, current_app, jsonify, request

# TODO: Zaimportuj tutaj: db, Host, RemoteClient oraz get_linux_metrics i get_windows_metrics
from app.extensions import db
from app.models import Host
from app.services.remote_client import RemoteClient
from app.services.system_info import get_linux_metrics, get_windows_metrics

api_bp = Blueprint("api_hosts", __name__)

# ==========================================
# CZĘŚĆ 1: CRUD (Twoje Zadanie)
# ==========================================


@api_bp.route("/hosts", methods=["GET"])
def get_hosts():  # return list of all hosts
    hosts = Host.query.all()
    return jsonify([h.to_dict() for h in hosts])


@api_bp.route("/hosts", methods=["POST"])
def add_host():  # add host to database
    data = request.get_json()
    if not data or "hostname" not in data or "ip_address" not in data:
        return jsonify({"error": "brak wymaganych pól"}), 400
    new_host = Host(
        hostname=data.get("hostname"),
        ip_address=data.get("ip_address"),
        os_type=data.get("os_type"),
    )
    try:
        db.session.add(new_host)
        db.session.commit()
        return jsonify(new_host.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)})


@api_bp.route("/hosts/<int:host_id>", methods=["DELETE"])
def delete_host(host_id):
    host = Host.query.get_or_404(host_id)
    try:
        db.session.delete(host)
        db.session.commit()
        return jsonify({"message": f"Host {host_id} usunięty"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==========================================
# CZĘŚĆ 2: MONITORING
# ==========================================


@api_bp.route("/hosts/<int:host_id>/ssh-info", methods=["GET"])
def get_ssh_info(host_id):
    """
    GOTOWIEC: Ten endpoint łączy się przez SSH z maszyną Vagrant/Linux.
    Analizuj ten kod, aby zrozumieć jak korzystać z current_app i serwisów.
    """
    # 1. Pobieramy hosta (odkomentuj po stworzeniu modelu Host)
    host = Host.query.get_or_404(host_id)

    # 2. Pobieramy konfigurację z current_app (ustawioną w config.py lub domyślną)
    # Zakładamy, że łączymy się do lokalnej maszyny wirtualnej Vagrant
    ssh_user = current_app.config.get("SSH_DEFAULT_USER", "vagrant")
    ssh_port = current_app.config.get("SSH_DEFAULT_PORT", 2222)
    ssh_key = current_app.config.get("SSH_KEY_FILE")  # np. ścieżka do private_key

    try:
        # Używamy Context Managera (with) do bezpiecznego otwarcia i zamknięcia połączenia
        # UWAGA: Odkomentuj import RemoteClient i get_linux_metrics na górze pliku!

        with RemoteClient(
            host.ip_address, ssh_user, port=ssh_port, key_file=ssh_key
        ) as client:
            data = get_linux_metrics(client)
            return jsonify(data), 200

    except Exception as e:
        print(f"SSH Error: {e}")
        return jsonify({"error": f"Błąd połączenia: {str(e)}"}), 500


@api_bp.route("/hosts/<int:host_id>/windows-info", methods=["GET"])
def get_windows_info(host_id):
    # 1. Pobierz hosta z bazy po ID (używając Host.query...)
    host = Host.query.filter_by(os_type="WINDOWS").get(host_id)

    try:
        # 3. Wywołaj funkcję get_windows_metrics() z pliku services/system_info.py
        data = get_windows_metrics()
        return jsonify(data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
