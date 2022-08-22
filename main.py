import matplotlib.pyplot as plt
import hashlib, os, shutil, stat
from dotenv import load_dotenv
from data_augmentation import augmentation

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
all_sessions = os.path.join(APP_ROOT, 'all_sessions_folder')
illegal_folder = os.path.join(APP_ROOT, 'illegal_folder')
legal_folder = os.path.join(APP_ROOT, 'legal_folder')
aug_illegal_folder = os.path.join(APP_ROOT, 'aug_illegal_folder')
aug_legal_folder = os.path.join(APP_ROOT, 'aug_legal_folder')


def clean_directory(path):
    if os.name == 'nt':
        for root, folders, files in os.walk(path):
            for folder in folders:
                os.chmod(os.path.join(root, folder), stat.S_IRWXU)
            for file in files:
                os.chmod(os.path.join(root, file), stat.S_IRWXU)

    return shutil.rmtree(path, ignore_errors=True)


def get_session(source_folder, destination_folder):
    for filename in os.walk(source_folder):
        for sub in os.listdir(filename[0]):
            if sub.startswith('session'):
                shutil.copy(os.path.join(filename[0], sub), destination_folder)


def discriminate_session(csv_url, source_folder):
    illegal_session = list()
    legal_session = list()

    with open(csv_url, 'r') as file:
        long_list = [line.strip() for line in file]
        for item in long_list:

            session = item.split(',')[0]
            value = item.split(',')[1]

            if int(value) == 0:
                legal_session.append(session)
            elif int(value) == 1:
                illegal_session.append(session)

    for session in legal_session:
        if session in os.listdir(source_folder):
            legal_session_path.append(os.path.join(all_sessions, session))

    for session in illegal_session:
        if session in os.listdir(source_folder):
            illegal_session_path.append(os.path.join(all_sessions, session))


def generate_plot(session_list, session_folder):
    for i, list_elm in enumerate(session_list):

        X_POSITION = 4
        Y_POSITION = 5

        move_x = list()
        move_y = list()

        drag_x = list()
        drag_y = list()

        click_x = list()
        click_y = list()

        released_x = list()
        released_y = list()

        with open(list_elm, 'r') as textFile:

            for line in textFile.readlines():

                if 'Move' in line:
                    move_x.append(line.split(",")[X_POSITION])
                    move_y.append(line.split(",")[Y_POSITION].replace('\n', ''))
                elif 'Pressed' in line:
                    click_x.append(line.split(",")[X_POSITION])
                    click_y.append(line.split(",")[Y_POSITION].replace('\n', ''))
                elif 'Released' in line:
                    released_x.append(line.split(",")[X_POSITION])
                    released_y.append(line.split(",")[Y_POSITION].replace('\n', ''))
                elif 'Drag' in line:
                    drag_x.append(line.split(",")[X_POSITION])
                    drag_y.append(line.split(",")[Y_POSITION].replace('\n', ''))

            fig = plt.figure()
            gs = fig.add_gridspec(2, 2, hspace=0, wspace=0)
            (ax1, ax2), (ax3, ax4) = gs.subplots()

            ax1.plot(move_x, move_y, c='g', label="Move")

            ax2.plot(drag_x, drag_y, c='b', label="Drag")

            ax3.scatter(click_x, click_y, c='r', marker="x", label="Click")

            ax4.scatter(released_x, released_y, c='y', marker="x", label="Released")

            # hide x and y axis

            ax1.axes.get_yaxis().set_visible(False)
            ax1.axes.get_xaxis().set_visible(False)

            ax2.axes.get_yaxis().set_visible(False)
            ax2.axes.get_xaxis().set_visible(False)

            ax3.axes.get_xaxis().set_visible(False)
            ax3.axes.get_yaxis().set_visible(False)

            ax4.axes.get_yaxis().set_visible(False)
            ax4.axes.get_xaxis().set_visible(False)

            # calculating hash of file to use as unique nam e of the image

            figure_name = hashlib.md5(open(list_elm, 'rb').read()).hexdigest()
            fig.savefig(os.path.join(session_folder, figure_name + '.png'), bbox_inches='tight', pad_inches=0)

            plt.close()


if __name__ == '__main__':

    dotenv_path = os.path.join(APP_ROOT, '.env')

    load_dotenv(dotenv_path)

    training_folder = os.environ.get('TRAINING_FOLDER_URL')
    test_folder = os.environ.get('TEST_FOLDER_URL')

    legal_session_path = list()
    illegal_session_path = list()

    print('Cleaning all folders...')

    clean_directory(all_sessions)
    clean_directory(illegal_folder)
    clean_directory(legal_folder)

    if not os.path.exists(all_sessions):
        os.makedirs(all_sessions)

    if not os.path.exists(illegal_folder):
        os.makedirs(illegal_folder)

    if not os.path.exists(aug_illegal_folder):
        os.makedirs(aug_illegal_folder)

    if not os.path.exists(legal_folder):
        os.makedirs(legal_folder)

    if not os.path.exists(aug_legal_folder):
        os.makedirs(aug_legal_folder)

    print('Collecting all sessions...')

    get_session(training_folder, all_sessions)
    get_session(test_folder, all_sessions)

    print('Discriminating all sessions...')

    discriminate_session('is_illegal.csv', all_sessions)

    print('Legal plot generation...')

    generate_plot(legal_session_path, legal_folder)

    print('Illegal plot generation...')

    generate_plot(illegal_session_path, illegal_folder)

    print('Augmentation is started...')

    augmentation(legal_folder, aug_legal_folder)
    augmentation(illegal_folder, aug_illegal_folder)

    print(f'Process ended. \n Number of plot illegal plot generated \
    {len([name for name in os.listdir(illegal_folder)])} \
     on {illegal_session_path.__len__()} \n Number of plot illegal plot generated \
     {len([name for name in os.listdir(legal_folder)])} on {legal_session_path.__len__()}')
