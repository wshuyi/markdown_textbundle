import sys
import re
import os
import shutil

def convert_pic_links_assets_repo(infile, outfile, local_repo_path):

    with open(infile) as f:
        data = f.read()

    links = re.findall(r'\!\[.*\]\((.*)\)', data)

    new_data = re.sub(r'\!\[(.*)\]\(' + local_repo_path + r'/(.+)\)', r'![\1](assets/\2)', data)

    with open(outfile, 'w') as f:
        f.write(new_data)
    
    return links





def sync_pics_to_assets_dir(links, assets_dir):
    for link in links:
        cmd = '/usr/bin/rsync -av {} {}'.format(link, assets_dir)
        os.system(cmd)

def make_info_json(textbundle_export_dir):
    text = '''
    {
  "transient" : true,
  "type" : "net.daringfireball.markdown",
  "creatorIdentifier" : "net.shinyfrog.bear",
  "version" : 2
}
    '''
    fout = "{}/info.json".format(textbundle_export_dir)
    with open(fout, 'w') as f:
        f.write(text)


def main(argv):
    if len(argv) == 2:
        textbundle_export_dir = os.path.expanduser("~/Downloads/my_textbundle.textbundle")
        local_repo_path = os.path.expanduser('~/Downloads/repo')
        if os.path.exists(textbundle_export_dir):
            shutil.rmtree(textbundle_export_dir)
        os.makedirs(textbundle_export_dir)
        assets_dir = "{}/assets".format(textbundle_export_dir)
        print(assets_dir)
        os.makedirs(assets_dir)
        infile = os.path.expanduser(argv[1])
        outfile = "{}/text.markdown".format(textbundle_export_dir)
        links = convert_pic_links_assets_repo(infile, outfile, local_repo_path)
        sync_pics_to_assets_dir(links, assets_dir)
        make_info_json(textbundle_export_dir)
    else:
        print('wrong argument number')

if __name__ == "__main__":
    main(sys.argv)

