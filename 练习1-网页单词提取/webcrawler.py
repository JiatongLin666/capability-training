import requests
import re
from bs4 import BeautifulSoup
import click
from urllib.parse import urlparse, urljoin

def get_html_of(url):
    resp = requests.get (url)
    if resp.status_code != 200:
        print(f'HTTP status code: {resp.status_code} returned, but 200 was expected. Exiting...')
        exit(1)
    return resp.content.decode()

def get_all_words_from(start_url, depth=0):
    """从 start_url 开始爬取，深度为 depth，返回所有单词列表。"""
    visited = set()
    words = []
    queue = [(start_url, 0)]
    base_domain = urlparse(start_url).netloc

    while queue:
        url, current_depth = queue.pop(0)
        if url in visited or current_depth > depth:
            continue
        visited.add(url)

        try:
            html = get_html_of(url)
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            continue

        soup = BeautifulSoup(html, 'html.parser')
        raw_text = soup.get_text()
        words.extend(re.findall(r'\w+', raw_text))

        # 如果还没到最大深度，继续收集同域链接
        if current_depth < depth:
            for link in soup.find_all('a', href=True):
                href = link['href']
                full_url = urljoin(url, href)
                # 只保留同一域名下的链接
                if urlparse(full_url).netloc == base_domain:
                    if full_url not in visited:
                        queue.append((full_url, current_depth + 1))

    return words

def count_occurrences_in(word_list):
    word_count={}
    for word in word_list:
        if word not in word_count:
            word_count[word] = 1
        else:
            current_count = word_count.get(word)  # 意思是获取当前这个word对应的键
            word_count[word] = current_count + 1
    return word_count

def get_top_words_from(word_count, length):
    occurrences = count_occurrences_in(word_count)
    filtered_occurrences = {
        word: count for word, count in occurrences.items()
        if len(word) > length
    }
    return sorted(filtered_occurrences.items(), key=lambda item: item[1], reverse=True)

def generate_password_variants(word):
    """生成常见密码变形：大小写、年份、数字符号后缀。"""
    variants = set()
    variants.add(word)
    variants.add(word.lower())
    variants.add(word.upper())
    variants.add(word.capitalize())

    # 常见后缀
    years = ['2019', '2020', '2021', '2022', '2023', '2024', '2025']
    symbols = ['!', '@', '#', '$', '1!', '2!', '3!', '01', '123', '123!']
    suffixes = years + symbols

    for suffix in suffixes:
        variants.add(word + suffix)
        variants.add(word.lower() + suffix)
        variants.add(word.upper() + suffix)
        variants.add(word.capitalize() + suffix)

    return sorted(variants)

@click.command()
@click.option('--url', '-u', prompt='Web URL', help='URL of webpage to extract from.')
@click.option('--length', '-l', default=0, help='Minimum length of words to extract (default 0, no limit).')
@click.option('--number', '-n', default=10, help='Number of words to extract (default 10).')
@click.option('--output', '-o', help='Output file name.')
@click.option('--depth', '-d', default=0, help='Crawl depth (default 0, only the given page).')
@click.option('--encryption', '-e', is_flag=True, default=False, help='Encryption mode (default False).')
def main(url, length, number, output, depth, encryption):
    all_words = get_all_words_from(url, depth)
    top_words = get_top_words_from(all_words, length)
    limit = min ((number, len(top_words)))

    lines = []
    for i in range(limit):
        word, count = top_words[i]
        if encryption:
            # 开启密码变形：输出变形后的候选密码
            lines.extend(generate_password_variants(word))
        else:
            # 未开启：输出 (word, count) 元组
            lines.append(f"{word}\t{count}")

    # 统一写入文件或打印到控制台
    if output:
        with open(output, 'w', encoding='utf-8') as f:
            for line in lines:
                f.write(line + '\n')
    else:
        for line in lines:
            print(line)

if __name__ == '__main__':
    main()