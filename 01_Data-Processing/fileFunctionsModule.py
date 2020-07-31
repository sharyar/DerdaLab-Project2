import os
import shutil
import glob
import pandas as pd


def searchMoveFiles(fileList, sourceDir, destDir):
    """If provided with a list of CSV files in the format:
    20150707-07DGplUD-OO-3, 20150707-07DGplUD-OO-3 etc
    copies these files from sourceDir to destDir
    Creates destination directory if it does not exist already.

    Args:
        fileList: List of strings contain filenames that need to be copies from
        source to dest directory
        sourceDir: source directory containing the files
        destDir: destination directory that the files need to be copied to
    """
    #   Clean file list to remove duplicates first:
    uniqueFileList = []
    filesMoved = []
    for file_ in fileList:
        if file_ not in uniqueFileList:
            uniqueFileList.append(file_)
    #   Create Dest directory if it does not exist:
    try:
        os.makedirs(destDir)
    except FileExistsError:
        pass

    #   Go through all the files in source directory and move files that show
    #   up in fileList provided.
    allFiles = glob.glob(os.path.join(sourceDir, "*.csv"))
    for file_ in allFiles:
        if (os.path.basename(file_)[:-4] in uniqueFileList):
            shutil.copy(file_, destDir)
            filesMoved.append(os.path.basename(file_)[:-4])
            uniqueFileList.remove(os.path.basename(file_)[:-4])

    print(f'# of Files Moved: {len(filesMoved)}')
    print('Files Moved:')
    print(*filesMoved, sep="\n")
    if len(uniqueFileList) > 0:
        print(f'Following files did not exist in source directory and were therefore not moved: \n\n{uniqueFileList}')


def importCSVMotifFilesAsDfFromDir(sourceDir):
    """Imports CSV files for trimer motifs from specified directory.

    Args:
        sourceDir (string): path to directory contain CSV files

    Returns:
        Pandas.DataFrame: DF contain combined columns from the CSV files.
    """
    allFiles = glob.glob(os.path.join(sourceDir, "*.csv"))
    df_full = pd.DataFrame()
    li = []
    li_counter = 0

    for file_ in allFiles:
        df = pd.read_csv(file_, index_col=0, header=0)
        cols = df.columns[~df.columns.isin(['motif'])]
        df.rename(columns = dict(
            zip(cols, str(os.path.basename(file_)[:-4])+'__' + cols)
            ), inplace=True)
        li.append(df)
        li_counter += 1

    df_full = pd.concat(li, axis=1)
    print(f'Imported: {li_counter} CSV Files \nResulting DF Structure: {df_full.shape}')
    return df_full


if __name__ == "__main__":
    pass