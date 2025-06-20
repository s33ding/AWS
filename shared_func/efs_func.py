import boto3

def delete_efs_access_points_by_pvc_uids(file_system_id, deleted_pv_uids):
    """
    Deleta os Access Points do EFS cujo path seja /pvc-<uid> e que estejam na lista fornecida.

    :param file_system_id: ID do EFS (ex: "fs-xxxxxxxxxxxxxxxxx")
    :param deleted_pv_uids: Lista de UIDs de PVCs deletados
    """
    efs = boto3.client("efs")

    response = efs.describe_access_points(FileSystemId=file_system_id)

    print(f"\n📄 Verificando Access Points para o File System: {file_system_id}\n")
    print(f"{'AccessPointId':<25} {'Path':<40} {'Match':<10}")
    print("-" * 80)

    deleted_count = 0

    for ap in response['AccessPoints']:
        ap_id = ap['AccessPointId']
        path = ap.get('RootDirectory', {}).get('Path', '')

        if not path.startswith("/pvc-"):
            continue

        uid = path.replace("/pvc-", "")
        if uid in deleted_pv_uids:
            print(f"{ap_id:<25} {path:<40} MATCH ✅")
            try:
                efs.delete_access_point(AccessPointId=ap_id)
                deleted_count += 1
            except Exception as e:
                print(f"❌ Erro ao deletar {ap_id}: {e}")
        else:
            print(f"{ap_id:<25} {path:<40} --")

    print(f"\n✅ {deleted_count} Access Points deletados com sucesso.")

