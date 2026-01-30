from nicegui import ui
import asyncio
import logging
from app.config.constants import BODY_STYLE, DETAILS_HEAD_HTML, TABLE_COLUMNS, LAYOUT_CONFIG
from app.services.data_service import get_cleaned_data

async def render_details_content(status: str = None):
    """完整保留原 details_page 的内部逻辑"""
    ui.query('body').style(BODY_STYLE)
    ui.add_head_html(DETAILS_HEAD_HTML)

    with ui.column().classes('w-full p-8 gap-6 items-center'):
        with ui.card().classes('w-full max-w-7xl p-8 rounded-[30px] shadow-2xl bg-white border-none overflow-hidden'):
            with ui.row().classes('w-full items-center justify-between mb-8'):
                with ui.row().classes('items-center gap-4'):
                    ui.element('div').classes('w-1.5 h-8 bg-blue-600 rounded-full')
                    with ui.column().classes('gap-1'):
                        ui.label('解析记录详情').classes('text-3xl font-black text-slate-800')
                        total_label = ui.label('DATABASE TOTAL: LOADING...').classes('text-[11px] text-blue-500/70 font-bold tracking-widest')
                with ui.row().classes('gap-3 items-center'):
                    search_input = ui.input(placeholder='检索词条...').props('rounded outlined dense').classes('w-80')
                    ui.button('导出 Excel', icon='download').props('elevated').classes('bg-blue-600 text-white px-6')

            table = ui.table(columns=TABLE_COLUMNS, rows=[], row_key='id').classes('w-full border-none shadow-none').props('flat no-data-label=" 暂无数据..." loading-label="正在努力加载中..." ')
            
            # 保持 Vue Slot 代码不变
            table.add_slot('body-cell-status', '''<q-td :props="props" class="text-center"><span :style="{'background-color': props.value?.includes('发布') ? '#ecfdf5' : props.value?.includes('拒绝') ? '#fef2f2' : props.value?.includes('审核') ? '#fff7ed' : '#f1f5f9', 'color': props.value?.includes('发布') ? '#059669' : props.value?.includes('拒绝') ? '#dc2626' : props.value?.includes('审核') ? '#d97706' : '#64748b', 'border': '1px solid currentColor', 'padding': '4px 12px', 'border-radius': '8px', 'font-weight': 'bold', 'display': 'inline-block', 'font-size': '12px', 'min-width': '80px'}">{{ props.value }}</span></q-td>''')
            table.add_slot('body-cell-actions', '''<q-td :props="props" class="text-center"><q-btn flat round color="blue-6" icon="manage_search" @click="$parent.$emit('view_details', props.row)"><q-tooltip class="bg-blue-800 text-white">查看解析详情</q-tooltip></q-btn></q-td>''')

            with ui.row().classes('w-full justify-end mt-8 items-center gap-4 px-4'):
                pagination = ui.pagination(min=1, max=1, direction_links=True).props('flat color=blue-7 size=md active-design=outline max-pages=5')
                with ui.row().classes('items-center gap-2 text-slate-500'):
                    ui.label('跳至').classes('text-sm')
                    jump_input = ui.number(value=1).props('outlined dense hide-bottom-space').classes('w-14 h-8 text-center bg-white')
                    ui.label('页').classes('text-sm')

    loading_lock = False

    async def load_data(page: int = 1):
        nonlocal loading_lock
        if loading_lock: return
        try: target_page = int(page)
        except: target_page = 1

        try:
            loading_lock = True
            table.props('loading')
            result = await asyncio.get_event_loop().run_in_executor(None, lambda: get_cleaned_data(page=target_page, status=status))
            page_size = LAYOUT_CONFIG.get('PAGE_SIZE', 15)
            for i, row in enumerate(result['rows']):
                row['index_id'] = (target_page - 1) * page_size + i + 1
            table.rows[:] = result['rows']
            total_label.text = f"DATABASE TOTAL: {result['total']} RECORDS"
            pagination.max = max(1, (result['total'] + page_size - 1) // page_size)
            if pagination.value != target_page: pagination.value = target_page 
            table.update()
        finally: 
            table.props(remove='loading')
            loading_lock = False

    pagination.on('update:modelValue', lambda e: load_data(page=e.args))
    jump_input.on('keydown.enter', lambda: load_data(page=jump_input.value))
    ui.timer(0.1, lambda: load_data(page=1), once=True)