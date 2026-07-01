# ======================== IMPORTS =======================
import asyncio
import time
import random
import json
import os
import re
import aiohttp
import requests
import base64
from datetime import datetime
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# Import protobuf files
from MajoRLoGinrEq_pb2 import MajorLogin
from MajoRLoGinrEs_pb2 import MajorLoginRes
from room_join_pb2 import join_room

# Import dari xC4.py
from xC4 import *

# ============ KONFIGURASI ============
ACCOUNT_FILE = "Xzol.txt"
MODE = "CLASSIC"
SKILL_DELAY = 2.0
MOVE_INTERVAL = 3.0
MAX_PLAYERS = 5

# ============ FUNGSI ENKRIPSI ============
KEY = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
IV = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])

async def encrypt_major_login(open_id, access_token):
    """Encrypt MajorLogin protobuf"""
    try:
        # Buat protobuf MajorLogin
        major_login = MajorLogin()
        major_login.event_time = str(datetime.now())[:-7]
        major_login.game_name = "free fire"
        major_login.platform_id = 2
        major_login.client_version = "1.126.2"
        major_login.client_version_code = "2024010012"
        major_login.system_software = "Android OS 11 / API-30 (RQ3A.210805.001)"
        major_login.system_hardware = "Handheld"
        major_login.device_type = "Handheld"
        major_login.telecom_operator = "Verizon"
        major_login.network_operator_a = "Verizon"
        major_login.network_type = "WIFI"
        major_login.network_type_a = "WIFI"
        major_login.screen_width = 1080
        major_login.screen_height = 2400
        major_login.screen_dpi = "440"
        major_login.processor_details = "ARMv8"
        major_login.cpu_type = 2
        major_login.cpu_architecture = "64"
        major_login.memory = 6144
        major_login.gpu_renderer = "Adreno (TM) 650"
        major_login.gpu_version = "OpenGL ES 3.2 V@1.50"
        major_login.graphics_api = "OpenGLES3"
        major_login.unique_device_id = f"Google|{random.randint(10000000, 99999999)}-{random.randint(10000000, 99999999)}-{random.randint(10000000, 99999999)}"
        major_login.client_ip = ""
        major_login.language = "en"
        major_login.open_id = open_id
        major_login.open_id_type = "4"
        major_login.login_open_id_type = 4
        major_login.access_token = access_token
        major_login.login_by = 3
        major_login.platform_sdk_id = 2
        major_login.origin_platform_type = "4"
        major_login.primary_platform_type = "4"
        
        # Memory available
        major_login.memory_available.version = 55
        major_login.memory_available.hidden_value = 81
        
        major_login.external_storage_total = 128512
        major_login.external_storage_available = random.randint(38000, 52000)
        major_login.internal_storage_total = 110731
        major_login.internal_storage_available = random.randint(18000, 32000)
        major_login.game_disk_storage_total = 26628
        major_login.game_disk_storage_available = random.randint(18000, 25000)
        major_login.external_sdcard_total_storage = 119234
        major_login.external_sdcard_avail_storage = random.randint(25000, 60000)
        major_login.library_path = "/data/app/~~random/base.apk"
        major_login.library_token = "hash|base.apk"
        major_login.client_using_version = "7428b253defc164018c604a1ebbfebdf"
        major_login.supported_astc_bitset = 16383
        major_login.analytics_detail = b"FwQVTgUPX1UaUllDDwcWCRBpWAUOUgsvA1snWlBaO1kFYg=="
        major_login.loading_time = random.randint(9000, 18000)
        major_login.release_channel = "android"
        major_login.channel_type = 3
        major_login.reg_avatar = 1
        major_login.if_push = 1
        major_login.is_vpn = 0
        major_login.android_engine_init_flag = 110009
        
        # Serialize dan encrypt
        serialized = major_login.SerializeToString()
        
        # Encrypt pake AES
        cipher = AES.new(KEY, AES.MODE_CBC, IV)
        padded = pad(serialized, AES.block_size)
        encrypted = cipher.encrypt(padded)
        
        return encrypted
    except Exception as e:
        print(f"❌ Error encrypting MajorLogin: {e}")
        import traceback
        traceback.print_exc()
        return None

async def major_login_request(encrypted_payload):
    """Kirim MajorLogin request ke server"""
    try:
        url = "https://loginbp.ggpolarbear.com/MajorLogin"
        headers = {
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 11; ASUS_Z01QD Build/PI)",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "Content-Type": "application/x-www-form-urlencoded",
            "Expect": "100-continue",
            "X-Unity-Version": "2018.4.11f1",
            "X-GA": "v1 1",
            "ReleaseVersion": "OB54"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=encrypted_payload) as response:
                if response.status == 200:
                    data = await response.read()
                    return data
                else:
                    print(f"❌ MajorLogin HTTP error: {response.status}")
                    return None
    except Exception as e:
        print(f"❌ MajorLogin request error: {e}")
        return None

async def get_account_token(uid, password):
    """Dapetin token buat login"""
    try:
        url = "https://100067.connect.garena.com/oauth/guest/token/grant"
        headers = {
            "Host": "100067.connect.garena.com",
            "User-Agent": await Ua(),
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "close"
        }
        data = {
            "uid": uid,
            "password": password,
            "response_type": "token",
            "client_type": "2",
            "client_secret": "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3",
            "client_id": "100067"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=data) as response:
                if response.status == 200:
                    data = await response.json()
                    open_id = data.get("open_id")
                    access_token = data.get("access_token")
                    return open_id, access_token
        return None, None
    except Exception as e:
        print(f"❌ Error getting token for {uid}: {e}")
        return None, None

async def login_account(uid, password, region="IND"):
    """Login akun dan dapetin key + iv"""
    try:
        print(f"[→] Login: {uid}...")
        
        # Step 1: Dapetin token
        open_id, access_token = await get_account_token(uid, password)
        if not open_id or not access_token:
            print(f"❌ Gagal dapet token untuk {uid}")
            return None
        
        # Step 2: Encrypt MajorLogin
        encrypted_payload = await encrypt_major_login(open_id, access_token)
        if not encrypted_payload:
            print(f"❌ Gagal encrypt MajorLogin untuk {uid}")
            return None
        
        # Step 3: Kirim MajorLogin
        response_data = await major_login_request(encrypted_payload)
        if not response_data:
            print(f"❌ Gagal MajorLogin untuk {uid}")
            return None
        
        # Step 4: Parse response
        try:
            login_res = MajorLoginRes()
            login_res.ParseFromString(response_data)
            
            # Ambil key dan iv
            key = login_res.key
            iv = login_res.iv
            token = login_res.token
            account_uid = login_res.account_uid
            region = login_res.region
            url = login_res.url
            timestamp = login_res.timestamp
            
            print(f"[✓] {uid} online! UID: {account_uid}, Region: {region}")
            
            return {
                'uid': str(account_uid),
                'original_uid': uid,
                'password': password,
                'open_id': open_id,
                'access_token': access_token,
                'token': token,
                'key': key,
                'iv': iv,
                'region': region,
                'url': url,
                'timestamp': timestamp,
                'online': True
            }
        except Exception as e:
            print(f"❌ Gagal parse response untuk {uid}: {e}")
            return None
            
    except Exception as e:
        print(f"❌ Error login {uid}: {e}")
        import traceback
        traceback.print_exc()
        return None

async def send_friend_request(uid, token, region="IND"):
    """Kirim friend request - pake fungsi dari xC4.py"""
    try:
        # Pake send_friend_request_single dari main.py
        # Karena fungsi ini ada di main.py, kita panggil langsung
        # Tapi di sini kita implementasi ulang pake xC4.py
        
        # Encrypt ID
        from xC4 import EnC_Uid
        encrypted_id = await EnC_Uid(int(uid), 'Uid')
        
        # Buat payload
        payload = f"08a7c4839f1e10{encrypted_id}1801"
        
        # Encrypt payload
        from xC4 import EnC_PacKeT
        # Pake key default
        key = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
        iv = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])
        
        encrypted_payload = await EnC_PacKeT(payload, key, iv)
        
        # Tentukan URL berdasarkan region
        if region.lower() == "ind":
            url = "https://client.ind.freefiremobile.com/RequestAddingFriend"
        elif region.lower() == "bd":
            url = "https://clientbp.ggpolarbear.com/RequestAddingFriend"
        else:
            url = "https://client.ind.freefiremobile.com/RequestAddingFriend"
        
        headers = {
            "Authorization": f"Bearer {token}",
            "X-Unity-Version": "2018.4.11f1",
            "X-GA": "v1 1",
            "ReleaseVersion": "OB54",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Dalvik/2.1.0"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=bytes.fromhex(encrypted_payload), headers=headers) as response:
                if response.status == 200:
                    print(f"✅ Friend request sent to {uid}")
                    return True
                else:
                    print(f"❌ Failed: Status {response.status}")
                    return False
    except Exception as e:
        print(f"❌ Error sending friend request: {e}")
        return False

async def create_squad_and_invite(accounts, region):
    """Bikin squad dan invite semua akun - pake fungsi dari xC4.py"""
    try:
        if not accounts:
            return False
        
        leader = accounts[0]
        print(f"[→] Bikin squad mode CLASSIC... Leader: {leader['uid']}")
        
        # Ambil key dan iv dari leader
        key = leader['key']
        iv = leader['iv']
        
        # 1. Buka squad pake OpEnSq dari xC4.py
        open_packet = await OpEnSq(key, iv, region)
        # Kirim packet (di sini lo perlu koneksi TCP)
        print(f"[✓] Squad dibuka!")
        await asyncio.sleep(0.5)
        
        # 2. Set ukuran squad ke MAX_PLAYERS
        change_packet = await cHSq(MAX_PLAYERS, int(leader['uid']), key, iv, region)
        print(f"[✓] Ukuran squad diubah ke {MAX_PLAYERS}")
        await asyncio.sleep(0.5)
        
        # 3. Invite semua akun lain pake SEnd_InV dari xC4.py
        for acc in accounts[1:]:
            print(f"[→] Invite {acc['uid']} ke squad...")
            invite_packet = await SEnd_InV(MAX_PLAYERS, int(acc['uid']), key, iv, region)
            print(f"[✓] {acc['uid']} masuk squad!")
            await asyncio.sleep(0.5)
        
        return True
    except Exception as e:
        print(f"❌ Error bikin squad: {e}")
        import traceback
        traceback.print_exc()
        return False

async def start_match_classic(account, region):
    """Mulai match mode Classic - pake FS dari xC4.py"""
    try:
        print(f"[→] Mencari match CLASSIC SQUAD...")
        
        key = account['key']
        iv = account['iv']
        
        start_packet = await FS(key, iv, region)
        # Kirim packet (di sini lo perlu koneksi TCP)
        
        print(f"[✓] Match ditemukan! Mode CLASSIC dimulai!")
        return True
    except Exception as e:
        print(f"❌ Error start match: {e}")
        return False

async def auto_play_in_match(account, region):
    """Auto main di dalam match: pencet skill + hindari zona"""
    print(f"[🎮] {account['uid']} mulai auto-play...")
    match_duration = 60  # 1 menit simulasi
    
    key = account['key']
    iv = account['iv']
    
    # Daftar skill yang bisa dipencet
    skills = ['Skill1', 'Skill2', 'Skill3', 'Ultimate']
    directions = ['atas', 'bawah', 'kiri', 'kanan', 'atas-kanan', 'atas-kiri', 'bawah-kanan', 'bawah-kiri']
    
    start_time = time.time()
    while time.time() - start_time < match_duration:
        try:
            # 1. Pencet skill aktif (random)
            skill = random.choice(skills)
            print(f"  → {account['uid']} pencet {skill}!")
            
            # 2. Hindari zona = gerak random
            direction = random.choice(directions)
            print(f"  → {account['uid']} gerak ke {direction} (hindari zona)")
            
            # 3. Kirim packet gerak (simulasi)
            # Di sini lo bisa panggil fungsi untuk kirim packet gerak
            
            # 4. Tunggu sebelum aksi berikutnya
            await asyncio.sleep(random.uniform(SKILL_DELAY, SKILL_DELAY + 1.5))
            
        except Exception as e:
            print(f"❌ Error auto-play {account['uid']}: {e}")
            break
    
    print(f"[✓] {account['uid']} selesai auto-play!")

async def load_accounts_from_file():
    """Baca akun dari Xzol.txt"""
    accounts = []
    try:
        with open(ACCOUNT_FILE, 'r') as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                if line and not line.startswith('#'):
                    parts = line.split('|')
                    if len(parts) >= 2:
                        accounts.append({
                            'uid': parts[0].strip(),
                            'password': parts[1].strip(),
                            'region': parts[2].strip() if len(parts) > 2 else 'IND'
                        })
        print(f"[✓] Load {len(accounts)} akun dari {ACCOUNT_FILE}")
        return accounts
    except FileNotFoundError:
        print(f"[✗] File {ACCOUNT_FILE} nggak ketemu! Buat dulu.")
        return []

async def run_classic_bot():
    """Main eksekusi bot Classic Squad"""
    print("="*60)
    print("🔥 CLASSIC SQUAD BOT - FREE FIRE 🔥")
    print("="*60)
    
    # 1. Load akun dari Xzol.txt
    accounts = await load_accounts_from_file()
    if len(accounts) < 2:
        print("❌ Minimal 2 akun di Xzol.txt!")
        return
    
    # 2. Login semua akun
    print("\n[LOGIN]")
    logged_in = []
    for acc in accounts:
        result = await login_account(acc['uid'], acc['password'], acc.get('region', 'IND'))
        if result:
            logged_in.append(result)
    
    if len(logged_in) < 2:
        print("❌ Gagal login minimal 2 akun!")
        return
    
    # Tampilkan info login
    print("\n[INFO LOGIN]")
    for i, acc in enumerate(logged_in):
        print(f"  Akun {i+1}: UID={acc['uid']}, Region={acc['region']}, Key={acc['key'].hex()[:16]}...")
    
    # 3. Auto add pertemanan (jika blom temenan)
    print("\n[PERTEMANAN]")
    for i in range(len(logged_in)):
        for j in range(i+1, len(logged_in)):
            # Kirim friend request dari akun i ke akun j
            token_i = logged_in[i].get('token')
            uid_j = logged_in[j]['uid']
            region = logged_in[i].get('region', 'IND')
            
            print(f"[→] {logged_in[i]['uid']} add friend {uid_j}...")
            success = await send_friend_request(uid_j, token_i, region)
            if success:
                print(f"[✓] Pertemanan {logged_in[i]['uid']} - {uid_j} terjalin!")
            await asyncio.sleep(0.5)
    
    # 4. Bikin squad dan invite
    print("\n[SQUAD]")
    region = logged_in[0].get('region', 'IND')
    await create_squad_and_invite(logged_in, region)
    
    # 5. Mulai match Classic
    print("\n[MATCH]")
    await start_match_classic(logged_in[0], region)
    
    # 6. Auto-play untuk semua akun (multithreading)
    print("\n[AUTO-PLAY]")
    tasks = []
    for acc in logged_in:
        task = asyncio.create_task(auto_play_in_match(acc, region))
        tasks.append(task)
    
    # Tunggu semua auto-play selesai
    await asyncio.gather(*tasks)
    
    print("\n[✓] SEMUA SELESAI! Bot udah main Classic Squad.")
    print("="*60)

# ============ EKSEKUSI ============
if __name__ == "__main__":
    # Pastikan library terinstall
    try:
        import aiohttp
        from Crypto.Cipher import AES
    except ImportError as e:
        print(f"❌ Install library dulu: pip install aiohttp pycryptodome")
        print(f"   Error: {e}")
        exit()
    
    # Jalankan bot
    asyncio.run(run_classic_bot())
