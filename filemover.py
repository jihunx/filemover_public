import os, shutil

# 이동할 파일들의 확장자를 입력합니다.
file_ext = (".dmg", ".zip")

# 경로가 지정돼 있지 않을 경우 기본으로 이동할 디렉터리를 입력합니다.
default_dir = r"/volume2/mac"

# 대상 디렉터리 절대 경로를 아래에 입력합니다. 경로 끝에 슬래시 입력하지 마세요.
target_dir = r"/volume2/downloads"

# 대상 디렉터리에 같은 이름의 파일이 있을 경우 이동할 디렉터리를 입력합니다.
dup_dir = r"/volume2/downloads/duplicated"

# filelist.txt 파일의 절대 경로
file_list = r"/volume1/homes/jihunx/filemover/filelist.txt"

# filelist.txt 리스트 순서를 정렬할지 여부 선택. True는 정렬한다. False면 안 한다.
sort_boolean = False


def get_strings(file):
    # filelist.txt에서 분류할 단어들을 가져온다(콤마 입력한 후 이동할 경로 지정).
    # 예1(1행) alfred,/volume2/mac/단일필수
    # 예2(2행) adguard

    # 설명
    # 예1) 해당 단어가 포함된 파일을 콤마 뒤 절대 경로로 이동
    # 예2) 단어는 있으나, 이동할 경로가 없는 경우 default_dir로 이동
    global strlist
    with open(file, 'r', encoding='utf-8-sig') as f:
        strlist = [i.strip() for i in f.readlines() if len(i) > 1]


def sorting(file):
    if sort_boolean:
        strlist.sort()
        with open(file, 'w') as ff:
            for item in strlist:
                ff.write("{}\n".format(item))


def filemove(filename, dst):
    # 파일 경에서 파일명만 반환
    tmp_file = os.path.basename(filename)

    # 옮길 디렉터리에 동일한 파일 이름 있는지 체크
    if tmp_file.lower() in [x.lower() for x in os.listdir(dst)]:
        # 동일한 파일 이름이 있는 경우 dup_dir 디렉터리로 파일 이동
        # dup_dir 디렉터리가 없는 경우 새로 생성
        if os.path.exists(dup_dir):
            shutil.move(filename, dup_dir)

        else:
            os.mkdir(dup_dir)
            shutil.move(filename, dup_dir)

    else:
        # 동일한 파일 이름이 존재하지 않으면 대상 디렉터리로 파일 이동
        shutil.move(filename, dst)
        print("[File moved] {} ===> {}".format(filename, dst))


def search(dirname):
    # 대상 디렉터리에서 디렉터리 리스트와 파일 리스트 생성
    try:
        folderlist = []
        filelist = []

        filenames = os.listdir(dirname)
        for filename in filenames:
            full_filename = os.path.join(dirname, filename)
            if os.path.isdir(full_filename):
                folderlist.append(full_filename)
                continue
            else:
                filelist.append(full_filename)

    except PermissionError:
        pass

    # 파일 리스트에서 파일 한 개 꺼내서
    for filename in filelist:
        # 지정 문자열 한 개를 꺼내서
        for str in strlist:

            lst_str = str.split(',')

            # 지정한 문자열의 파일이 있을 때
            if lst_str[0].lower() in filename.lower() and filename.endswith(file_ext):
                # 이동할 경로가 지정된 경우
                if len(lst_str) > 1:
                    filemove(filename, lst_str[1])
                    # filename은 하나만 존재할 것이므로 현재 반복문 중지하고 그 다음 filename으로 이동
                    break
                # 이동할 경로가 지정되지 않은 경우
                else:
                    filemove(filename, default_dir)
                    # filename은 하나만 존재할 것이므로 현재 반복문 중지하고 그 다음 filename으로 이동
                    break

            continue


get_strings(file_list)

search(target_dir)

sorting(file_list)
