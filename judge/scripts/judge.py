from posix import environ
from pika import connection
import os
import pymysql.cursors
import psutil
import shutil
import subprocess
import glob
import datetime
from threading import Timer


def get_connection():
    host = os.environ.get("DB_HOST")
    user = os.environ.get("DB_USER")
    passwd = os.environ.get("DB_PASSWORD")
    database = os.environ.get("DB_NAME")
    return pymysql.connect(host=host, user=user, password=passwd, database=database, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)


def judge(id):
    with get_connection() as connection:
        with connection.cursor() as cur:
            cur.execute("SELECT * FROM submissions WHERE id = %s", (id,))
            submission_info = dict(cur.fetchone())
            cur.execute(
                "SELECT * FROM problems WHERE id = %s", (
                    submission_info["problem_id"],)
            )

            try:
                problem_info = dict(cur.fetchone())
                cur.execute(
                    "SELECT * FROM testcases WHERE problem_id = %s", (
                        submission_info["problem_id"],)
                )
                cases = cur.fetchall()
                dir_name = "/root/tmp_{}".format(id)
                os.makedirs(dir_name)
                exefile = dir_name + "/{}.py".format(id)
                with open(exefile, mode="w") as f:
                    f.write(submission_info["code"])

                ac = 0
                tle = 0
                wa = 0
                re = 0
                status_all = "WJ..."

                for index,case in enumerate(cases):
                    command = "python3 " + exefile
                    process = psutil.Popen(
                        command,
                        shell=True,
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                    )
                    memory_limit = float(problem_info["memory_limit"])
                    time_limit = float(problem_info["time_limit"])
                    print(
                        "time_limit: {}, memory_limit: {}".format(
                            time_limit, memory_limit
                        )
                    )
                    status = "WJ..."
                    memoryusage = 0
                    spent_time = 0
                    datetime1 = datetime.datetime.now().timestamp() * 1000
                    my_timer = Timer(time_limit * 1.1, process.kill)
                    try:
                        my_timer.start()
                        case_memory_usage = process.memory_info().rss / 1024
                        output, error = process.communicate(
                            case['content'].encode())
                        memoryusage = max(
                            memoryusage, case_memory_usage
                        )
                    finally:
                        my_timer.cancel()
                        datetime2 = datetime.datetime.now().timestamp() * 1000

                    case_time = datetime2 - datetime1
                    # print("output:{}".format(output.decode()))
                    # print("answer:{}".format(out_context))

                    if case_time > time_limit * 1000:
                        tle += 1
                        status = "TLE"
                    elif process.returncode != 0:
                        re += 1
                        status = "RE"
                        print(error)
                    elif output.decode().rstrip() == case['answer'].rstrip():
                        ac += 1
                        status = "AC"
                    else:
                        wa += 1
                        status = "WA"
                    spent_time = max(spent_time, case_time)
                    print('case {}: {}'.format(index,status))
                    print('time :{}'.format(case_time))
                    print('memory :{}'.format(case_memory_usage))
                    print('input :{}'.format(case['content']))
                    print('output :{}'.format(output.decode().rstrip()))
                    print('expected :{}'.format(case['answer'].rstrip()))
                    


                    if status == "WA":
                        status_all = "WA"
                    if status == "RE" and status_all != "WA":
                        status_all = "RE"
                    if status == "TLE" and status_all != "WA" and status_all != "RE":
                        status_all = "TLE"

                    cur.execute(
                        "UPDATE submissions SET ac = %s, wa = %s, tle = %s, re = %s, status = %s WHERE id = %s",
                        (
                            ac,
                            wa,
                            tle,
                            re,
                            status_all,
                            submission_info["id"],
                        ),
                    )
                    connection.commit()
            finally:
                if status_all == "WJ...":
                    status_all = "AC"
                cur.execute(
                    "UPDATE submissions SET ac = %s, wa = %s, tle = %s, re = %s, status = %s WHERE id = %s",
                    (
                        ac,
                        wa,
                        tle,
                        re,
                        status_all,
                        submission_info["id"],
                    ),
                )
                connection.commit()
