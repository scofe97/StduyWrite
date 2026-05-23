// Nexus Web File Manager
const state = { nexusUrl: '', auth: '', currentRepo: '', continuationToken: null };

function getAuth() {
  const user = document.getElementById('username').value;
  const pass = document.getElementById('password').value;
  return 'Basic ' + btoa(user + ':' + pass);
}

function showMessage(text, isError) {
  const el = document.getElementById('message');
  el.textContent = text;
  el.className = isError ? 'message error' : 'message success';
  setTimeout(() => { el.textContent = ''; el.className = 'message'; }, 5000);
}

async function connect() {
  state.nexusUrl = document.getElementById('nexusUrl').value.replace(/\/$/, '');
  state.auth = getAuth();
  try {
    const res = await fetch(state.nexusUrl + '/service/rest/v1/repositories', {
      headers: { 'Authorization': state.auth }
    });
    if (!res.ok) throw new Error('HTTP ' + res.status);
    const repos = await res.json();
    const select = document.getElementById('repoSelect');
    select.innerHTML = '<option value="">-- 리포지토리 선택 --</option>';
    repos.forEach(r => {
      const opt = document.createElement('option');
      opt.value = r.name;
      opt.textContent = r.name + ' (' + r.format + '/' + r.type + ')';
      select.appendChild(opt);
    });
    showMessage('연결 성공: ' + repos.length + '개 리포지토리');
  } catch (e) {
    showMessage('연결 실패: ' + e.message, true);
  }
}

async function loadComponents(append) {
  const repo = document.getElementById('repoSelect').value;
  if (!repo) return showMessage('리포지토리를 선택하세요', true);
  state.currentRepo = repo;

  let url = state.nexusUrl + '/service/rest/v1/components?repository=' + repo;
  if (append && state.continuationToken) {
    url += '&continuationToken=' + state.continuationToken;
  }

  try {
    const res = await fetch(url, { headers: { 'Authorization': state.auth } });
    if (!res.ok) throw new Error('HTTP ' + res.status);
    const data = await res.json();
    state.continuationToken = data.continuationToken;

    const tbody = document.getElementById('fileList');
    if (!append) tbody.innerHTML = '';

    data.items.forEach(item => {
      item.assets.forEach(asset => {
        const tr = document.createElement('tr');
        const size = asset.fileSize ? (asset.fileSize / 1024).toFixed(1) + ' KB' : '-';
        const date = asset.lastModified ? new Date(asset.lastModified).toLocaleString() : '-';
        tr.innerHTML =
          '<td>' + asset.path + '</td>' +
          '<td>' + size + '</td>' +
          '<td>' + date + '</td>' +
          '<td>' +
            '<button onclick="downloadAsset(\'' + asset.downloadUrl + '\')">Download</button> ' +
            '<button class="danger" onclick="deleteComponent(\'' + item.id + '\')">Delete</button>' +
          '</td>';
        tbody.appendChild(tr);
      });
    });

    document.getElementById('loadMore').style.display = state.continuationToken ? 'block' : 'none';
    showMessage(data.items.length + '개 컴포넌트 로드');
  } catch (e) {
    showMessage('로드 실패: ' + e.message, true);
  }
}

async function searchComponents() {
  const keyword = document.getElementById('searchInput').value;
  if (!keyword) return loadComponents(false);

  let url = state.nexusUrl + '/service/rest/v1/search?keyword=' + encodeURIComponent(keyword);
  if (state.currentRepo) url += '&repository=' + state.currentRepo;

  try {
    const res = await fetch(url, { headers: { 'Authorization': state.auth } });
    if (!res.ok) throw new Error('HTTP ' + res.status);
    const data = await res.json();

    const tbody = document.getElementById('fileList');
    tbody.innerHTML = '';

    data.items.forEach(item => {
      item.assets.forEach(asset => {
        const tr = document.createElement('tr');
        const size = asset.fileSize ? (asset.fileSize / 1024).toFixed(1) + ' KB' : '-';
        tr.innerHTML =
          '<td>' + asset.path + '</td>' +
          '<td>' + size + '</td>' +
          '<td>' + (asset.lastModified ? new Date(asset.lastModified).toLocaleString() : '-') + '</td>' +
          '<td><button onclick="downloadAsset(\'' + asset.downloadUrl + '\')">Download</button></td>';
        tbody.appendChild(tr);
      });
    });
    showMessage('검색 결과: ' + data.items.length + '개');
  } catch (e) {
    showMessage('검색 실패: ' + e.message, true);
  }
}

async function uploadFile() {
  const fileInput = document.getElementById('fileInput');
  const directory = document.getElementById('uploadDir').value || '/';
  const repo = document.getElementById('repoSelect').value;

  if (!repo) return showMessage('리포지토리를 선택하세요', true);
  if (!fileInput.files.length) return showMessage('파일을 선택하세요', true);

  const file = fileInput.files[0];
  const formData = new FormData();
  formData.append('raw.directory', directory);
  formData.append('raw.asset1', file);
  formData.append('raw.asset1.filename', file.name);

  try {
    const res = await fetch(
      state.nexusUrl + '/service/rest/v1/components?repository=' + repo,
      { method: 'POST', headers: { 'Authorization': state.auth }, body: formData }
    );
    if (!res.ok) {
      const text = await res.text();
      throw new Error('HTTP ' + res.status + ': ' + text);
    }
    showMessage('업로드 성공: ' + file.name);
    fileInput.value = '';
    loadComponents(false);
  } catch (e) {
    showMessage('업로드 실패: ' + e.message, true);
  }
}

function downloadAsset(url) {
  window.open(url, '_blank');
}

async function deleteComponent(id) {
  if (!confirm('정말 삭제하시겠습니까?')) return;
  try {
    const res = await fetch(
      state.nexusUrl + '/service/rest/v1/components/' + id,
      { method: 'DELETE', headers: { 'Authorization': state.auth } }
    );
    if (!res.ok) throw new Error('HTTP ' + res.status);
    showMessage('삭제 완료');
    loadComponents(false);
  } catch (e) {
    showMessage('삭제 실패: ' + e.message, true);
  }
}
