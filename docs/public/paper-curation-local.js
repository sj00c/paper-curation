function toggleTopic(id) {
      const body = document.getElementById(id);
      const toggle = document.getElementById('toggle-' + id);
      body.classList.toggle('collapsed');
      toggle.textContent = body.classList.contains('collapsed') ? '\\u25B6' : '\\u25BC';
      if (!body.classList.contains('collapsed')) setTimeout(lazyLoad, 100);
    }
    function toggleSub(id) {
      const body = document.getElementById(id);
      const toggle = document.getElementById('toggle-' + id);
      body.classList.toggle('collapsed');
      toggle.textContent = body.classList.contains('collapsed') ? '\\u25B6' : '\\u25BC';
      if (!body.classList.contains('collapsed')) setTimeout(lazyLoad, 100);
    }
    function toggleInsights() {
      const body = document.getElementById('insights-body');
      if (!body) return;
      const toggle = document.getElementById('toggle-insights-body');
      const header = document.querySelector('.insights-header');
      const collapsed = body.classList.toggle('collapsed');
      if (toggle) toggle.textContent = collapsed ? '\\u25B6' : '\\u25BC';
      if (header) header.classList.toggle('open', !collapsed);
    }
    function sortCards(key, order, trigger) {
      document.querySelectorAll('.topic-body').forEach(body => {
        const cards = [...body.querySelectorAll('.paper-card')];
        cards.sort((a, b) => {
          let va, vb;
          if (key === 'date') { va = a.dataset.date || ''; vb = b.dataset.date || ''; }
          else { va = parseFloat(a.dataset.score) || 0; vb = parseFloat(b.dataset.score) || 0; }
          if (order === 'asc') return va > vb ? 1 : va < vb ? -1 : 0;
          return va < vb ? 1 : va > vb ? -1 : 0;
        });
        cards.forEach(c => body.appendChild(c));
      });
      document.querySelectorAll('.sort-btn').forEach(b => b.classList.remove('active'));
      if (trigger) trigger.classList.add('active');
      setTimeout(lazyLoad, 100);
    }
    function lazyLoad() {
      const imgs = document.querySelectorAll('img.lazy:not(.loaded)');
      if ('IntersectionObserver' in window) {
        const obs = new IntersectionObserver((entries) => {
          entries.forEach(e => {
            if (e.isIntersecting) {
              const img = e.target; img.src = img.dataset.src;
              img.classList.add('loaded'); obs.unobserve(img);
            }
          });
        }, {rootMargin: '200px'});
        imgs.forEach(img => obs.observe(img));
      } else { imgs.forEach(img => { img.src = img.dataset.src; img.classList.add('loaded'); }); }
    }
    document.addEventListener('DOMContentLoaded', lazyLoad);

    // Search
    const NO_RESULTS_GUIDANCE = '검색 결과가 없습니다. 해당 저자가 포함된 다른 토픽에서 다시 시도해보세요. 논문 검색은 다른 구성 토픽에서 다시 시도해보세요. No results found. Try another configured topic containing this author or paper.';
    function searchPapers(query) {
      const q = query.trim().toLowerCase();
      const groups = document.querySelectorAll('.topic-group');
      const countEl = document.querySelector('.search-count');
      if (!q) {
        groups.forEach(g => { g.style.display = '';
          g.querySelectorAll('.paper-card').forEach(c => c.style.display = '');
          const body = g.querySelector('.topic-body');
          if (body) { body.classList.add('collapsed'); }
          const toggle = g.querySelector('.topic-toggle');
          if (toggle) toggle.textContent = '\\u25B6';
        });
        if (countEl) countEl.style.display = 'none';
        return;
      }
      let total = 0;
      groups.forEach(g => {
        let catMatched = 0;
        const subs = g.querySelectorAll('.sub-group');
        if (subs.length > 0) {
          subs.forEach(sg => {
            const cards = sg.querySelectorAll('.paper-card');
            let subMatched = 0;
            cards.forEach(c => {
              const text = c.textContent.toLowerCase();
              if (text.includes(q)) { c.style.display = ''; subMatched++; }
              else { c.style.display = 'none'; }
            });
            if (subMatched > 0) {
              sg.style.display = '';
              const subBadge = sg.querySelector('.sub-count');
              if (subBadge) subBadge.textContent = subMatched;
            } else {
              sg.style.display = 'none';
            }
            // Keep sub-category collapsed — user clicks to expand
            const subBody = sg.querySelector('.sub-body');
            if (subBody) subBody.classList.add('collapsed');
            const subToggle = sg.querySelector('.sub-toggle');
            if (subToggle) subToggle.textContent = '\\u25B6';
            catMatched += subMatched;
          });
        } else {
          g.querySelectorAll('.paper-card').forEach(c => {
            const text = c.textContent.toLowerCase();
            if (text.includes(q)) { c.style.display = ''; catMatched++; }
            else { c.style.display = 'none'; }
          });
        }
        if (catMatched > 0) {
          g.style.display = '';
          // Keep category collapsed — only update count badge
          const body = g.querySelector('.topic-body');
          if (body) body.classList.add('collapsed');
          const toggle = g.querySelector('.topic-toggle');
          if (toggle) toggle.textContent = '\\u25B6';
          const badge = g.querySelector('.topic-count');
          if (badge) badge.textContent = catMatched + '\\ud3b8';
          total += catMatched;
        } else {
          g.style.display = 'none';
        }
      });
      if (countEl) { countEl.textContent = total > 0 ? total + ' results' : NO_RESULTS_GUIDANCE; countEl.style.display = 'block'; }
      setTimeout(lazyLoad, 100);
    }
    let searchTimer;
    document.addEventListener('DOMContentLoaded', function() {
      const input = document.getElementById('search-input');
      if (input) input.addEventListener('input', function() {
        if (window._searchMode === 'deep') return;
        clearTimeout(searchTimer);
        searchTimer = setTimeout(() => searchPapers(this.value), 300);
      });
    });

    // Lightbox
    document.addEventListener('DOMContentLoaded', function() {
      const lb = document.getElementById('lightbox');
      const lbImg = document.getElementById('lightbox-img');
      if (!lb || !lbImg) return;
      document.addEventListener('click', function(e) {
        const img = e.target.closest('.paper-fig img, .category-timeline img, .timeline-section img');
        if (img) {
          const src = img.dataset.src || img.src;
          if (src) { lbImg.src = src; lb.classList.add('active'); }
        }
      });
      lb.addEventListener('click', function() { lb.classList.remove('active'); lbImg.src = ''; });
      document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && lb.classList.contains('active')) { lb.classList.remove('active'); lbImg.src = ''; }
      });
    });

    // Server-authoritative local actions. This dashboard never holds credentials
    // and never contacts an AI provider from the browser.
    const ACTION = { bootstrap: null, current: null };
    function actionStatus(text, isError) {
      const el = document.getElementById('deep-status');
      if (!el) return;
      el.textContent = text || '';
      el.classList.toggle('active', Boolean(text));
      el.classList.toggle('error', Boolean(isError));
    }
    function actionJson(path, options) {
      return fetch(path, Object.assign({ credentials: 'same-origin' }, options || {})).then(async function(response) {
        let payload = null;
        try { payload = await response.json(); } catch (e) {}
        if (!response.ok) throw new Error((payload && payload.error) || ('Local action service returned ' + response.status));
        return payload || {};
      });
    }
    function actionIdempotencyKey() {
      const bytes = new Uint8Array(32);
      crypto.getRandomValues(bytes);
      return Array.prototype.map.call(bytes, function(byte) { return byte.toString(16).padStart(2, '0'); }).join('');
    }
    function actionInput(command) {
      const query = (document.getElementById('search-input').value || '').trim();
      if (command === 'audio.create') return { auth_mode: 'auto', requested_target_seconds: 300, source: 'dashboard' };
      if (!query) throw new Error('Enter a question before starting a local action.');
      return { auth_mode: 'auto', query: query, source: 'dashboard' };
    }
    async function runLocalAction(command) {
      try {
        const input = actionInput(command);
        actionStatus('Preparing a server-authoritative plan…');
        const plan = await actionJson('/api/action/plan', {
          method: 'POST', headers: { 'content-type': 'application/json' },
          body: JSON.stringify({ schema: 1, command: command, topic_alias: ACTION.bootstrap.topic_alias, input: input, limits: {} })
        });
        if (!plan.operation_id || !plan.plan_hash) {
          actionStatus('This action is unavailable on the local server. Nothing was started.', true);
          return;
        }
        const preview = plan.preview ? '\\n\\n' + JSON.stringify(plan.preview, null, 2) : '';
        if (!window.confirm('Review the server plan and approve this local action?' + preview)) {
          actionStatus('Plan was not approved. Nothing was started.');
          return;
        }
        const approved = await actionJson('/api/action/approve', {
          method: 'POST', headers: { 'content-type': 'application/json' },
          body: JSON.stringify({ schema: 1, operation_id: plan.operation_id, plan_hash: plan.plan_hash, decision: 'approve' })
        });
        const started = await actionJson('/api/action/start', {
          method: 'POST', headers: { 'content-type': 'application/json', 'X-PC-Redeem': approved.redeem_credential || '', 'Idempotency-Key': actionIdempotencyKey() },
          body: JSON.stringify({ schema: 1, operation_id: plan.operation_id, plan_hash: plan.plan_hash })
        });
        ACTION.current = { operation_id: plan.operation_id, plan_hash: plan.plan_hash };
        await refreshActionState(started);
      } catch (error) {
        actionStatus((error && error.message) || 'Local action service is unavailable. Nothing was started.', true);
      }
    }
    async function refreshActionState(started) {
      if (!ACTION.current) return;
      try {
        const id = encodeURIComponent(ACTION.current.operation_id);
        const status = await actionJson('/api/action/status?operation_id=' + id);
        const final = await actionJson('/api/action/final?operation_id=' + id).catch(function() { return null; });
        const state = (final && final.state) || status.state || (started && started.state);
        if (state === 'RETAINED_NO_EFFECT') {
          actionStatus('The local server retained the approved plan but did not dispatch work. Nothing was changed.', true);
        } else {
          actionStatus(state ? ('Local action state: ' + state) : 'The local server accepted the action; check its status for results.');
        }
      } catch (error) {
        const state = started && started.state;
        actionStatus(state === 'RETAINED_NO_EFFECT'
          ? 'The local server retained the approved plan but did not dispatch work. Nothing was changed.'
          : 'The action status is unavailable; no browser fallback will run.', true);
      }
    }
    function configureAudio(capability) {
      const button = document.getElementById('deep-audio');
      if (!button) return;
      const enabled = Boolean(capability && capability.schema === 'AudioCapabilityV1' && capability.state === 'AVAILABLE');
      button.hidden = !enabled;
      button.disabled = !enabled;
      if (!enabled) button.setAttribute('aria-disabled', 'true'); else button.removeAttribute('aria-disabled');
    }
    document.addEventListener('DOMContentLoaded', async function() {
      const bootstrapEl = document.getElementById('dashboard-bootstrap');
      let embedded = { topic_alias: '' };
      try { embedded = JSON.parse(bootstrapEl.textContent); } catch (e) {}
      const normal = document.getElementById('deep-normal');
      const deeper = document.getElementById('deep-deeper');
      const audio = document.getElementById('deep-audio');
      [normal, deeper, audio].forEach(function(button) {
        if (button) { button.disabled = true; button.setAttribute('aria-disabled', 'true'); }
      });
      configureAudio(null);
      try {
        const authority = await actionJson('/api/bootstrap');
        ACTION.bootstrap = Object.assign({}, embedded, authority);
        const actionsAvailable = Boolean(
          ACTION.bootstrap.action_capability &&
          ACTION.bootstrap.action_capability.schema === 'ActionCapabilityV1' &&
          ACTION.bootstrap.action_capability.state === 'AVAILABLE'
        );
        [normal, deeper].forEach(function(button) {
          if (!button) return;
          button.disabled = !actionsAvailable;
          if (actionsAvailable) button.removeAttribute('aria-disabled');
          else button.setAttribute('aria-disabled', 'true');
        });
        configureAudio(actionsAvailable ? ACTION.bootstrap.audio_capability : null);
        if (!actionsAvailable) {
          actionStatus('Local action execution is unavailable; browsing remains available.', false);
        }
      } catch (error) {
        ACTION.bootstrap = null;
        actionStatus('Local action authority is unavailable. Nothing can be started.', true);
      }
      if (normal) normal.addEventListener('click', function() { runLocalAction('query.normal'); });
      if (deeper) deeper.addEventListener('click', function() { runLocalAction('query.deeper'); });
      if (audio) audio.addEventListener('click', function() { runLocalAction('audio.create'); });
      function invokeDashboardAction(target) {
        if (!target) return;
        const action = target.dataset.dashboardAction;
        if (action === 'toggle-insights') toggleInsights();
        if (action === 'toggle-topic') toggleTopic(target.dataset.target);
        if (action === 'toggle-sub') toggleSub(target.dataset.target);
        if (action === 'sort') sortCards(target.dataset.sortKey, target.dataset.sortDir, target);
      }
      document.addEventListener('click', function(event) {
        invokeDashboardAction(event.target.closest('[data-dashboard-action]'));
      });
      document.addEventListener('keydown', function(event) {
        if (event.key === 'Enter' || event.key === ' ') {
          const target = event.target.closest('[data-dashboard-action]');
          if (target) { event.preventDefault(); invokeDashboardAction(target); }
        }
      });
    });
