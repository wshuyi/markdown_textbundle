import sys
import re
import os


def convert_pic_links_local_repo(infile, outfile, local_repo_path):

    with open(infile) as f:
        data = f.read()

    links = re.findall(r'\!\[.*\]\((.*)\)', data)

    new_data = re.sub(r'\!\[(.*)\]\(.+/(.+)\)', r'![\1](' + local_repo_path + r'/\2)', data)

    with open(outfile, 'w') as f:
        f.write(new_data)
    
    return links

def sync_pics_to_local_repo(infile, links, local_repo_path):
    web_link_pattern = re.compile(r'(ht|f)tps?://')
    local_link_pattern = re.compile(r'^(\.*/)*(.*/)*(.*)')
    local_repo_link_pattern = re.compile(local_repo_path)
    
    for link in links:
        if web_link_pattern.search(link): # is a web link
            cmd = '/usr/local/bin/wget -c -P {} '.format(local_repo_path) + link
            try:
                os.system(cmd)
            except:
                print('can not download the link: {}'.format(link))
        elif local_link_pattern.search(link): # is a local link
            if local_repo_link_pattern.search(link): # is already a local repo link
                print('it is already in local repo, do nothing')
                pass
            else: # is a local link, but not in local repo
                if link.startswith('/'): #it is a absolute path
                    pass
                else: # it is a relevant path
                    source_path = re.search(r'.*/', infile).group()
                    if re.search(r'%.*/', link):
                        image_chinese_dir = re.search(r'.*/(.*)\..*', infile).group(1)
                        link = re.sub(r'.*(/.*)', image_chinese_dir+r'\1', link)
                    absolute_image_path = os.path.abspath(source_path + link)
                    link = absolute_image_path

                cmd = '/usr/bin/rsync -av {} {}'.format(link, local_repo_path)
                try:
                    os.system(cmd)
                except:
                    print('can not sync the link: {}'.format(link))
        else: # not a valid link
            print('do nothing for a invalid link: {}'.format(link))
            pass

def main(argv):
    if len(argv) == 2:
        local_repo_path = os.path.expanduser("~/Downloads/repo")
        if not os.path.exists(local_repo_path):
            os.makedirs(local_repo_path)
        infile = os.path.expanduser(argv[1])
        outfile = os.path.expanduser("~/Downloads/temp.md")
        num_vars = len(argv)
        links = convert_pic_links_local_repo(infile, outfile, local_repo_path)
        sync_pics_to_local_repo(infile, links, local_repo_path)
    else:
        print('wrong argument number')

if __name__ == "__main__":
    main(sys.argv)

