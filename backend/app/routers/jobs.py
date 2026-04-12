import asyncio
import os
import sys
import logging
from fastapi import APIRouter, BackgroundTasks, HTTPException
from ..core.setting import get_settings

logger = logging.getLogger(__name__)
router = APIRouter(tags=["Jobs"])
settings = get_settings()

async def run_script(script_path: str, script_name: str):
    """스크립트를 실행하고 출력을 실시간으로 로그에 남기는 함수"""
    python_executable = sys.executable
    
    if not os.path.exists(script_path):
        logger.error(f"❌ {script_name} 파일을 찾을 수 없음: {script_path}")
        return False

    logger.info(f"▶️ {script_name} 시작...")
    
    # 서브프로세스 생성 (stdout을 PIPE로 설정)
    process = await asyncio.create_subprocess_exec(
        python_executable, "-u", script_path,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    # 실시간 로그 출력을 위한 비동기 스트림 리더
    async def log_stream(stream, prefix):
        while True:
            line = await stream.readline()
            if not line:
                break
            # 바이트를 문자열로 디코딩하고 공백 제거 후 출력
            decoded_line = line.decode().strip()
            if decoded_line:
                logger.info(f"[{prefix}] {decoded_line}")

    # stdout과 stderr를 동시에 감시
    await asyncio.gather(
        log_stream(process.stdout, script_name),
        log_stream(process.stderr, f"{script_name} ERROR")
    )

    # 프로세스 종료 대기
    return_code = await process.wait()

    if return_code != 0:
        logger.error(f"❌ {script_name} 실패 (Return Code: {return_code})")
        return False
    
    logger.info(f"✅ {script_name} 정상 종료")
    return True

async def run_scripts_in_background_async():
    """데이터 수집 -> 통계 처리 순차 실행"""
    try:
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        collector_path = os.path.join(base_dir, 'data-collector', 'collect_data.py')
        processor_path = os.path.join(base_dir, 'data-collector', 'process_stats.py')

        logger.info(f">> 백그라운드 작업 파이프라인 시작 (Base: {base_dir})")

        # 1. 데이터 수집
        success = await run_script(collector_path, "Data Collector")
        if not success:
            logger.error("⛔ 수집기 실패로 인해 통계 처리를 중단합니다.")
            return

        # 2. 통계 처리 (수집이 성공했을 때만 실행)
        await run_script(processor_path, "Stat Processor")

        logger.info("🎉 모든 백그라운드 작업 완료.")

    except Exception as e:
        logger.error(f"비동기 작업 중 치명적 오류: {e}", exc_info=True)

@router.post("/run-scheduled-jobs/{secret_key}")
async def run_scheduled_jobs(secret_key: str, background_tasks: BackgroundTasks):
    if secret_key != settings.SCHEDULER_SECRET_KEY:
        raise HTTPException(status_code=403, detail="Unauthorized")
    
    background_tasks.add_task(run_scripts_in_background_async)
    logger.info("스케줄 작업 요청 수신. 백그라운드 실행 시작.")
    return {"status": "success", "message": "Scheduled jobs started."}