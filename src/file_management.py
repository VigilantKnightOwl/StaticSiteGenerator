from datetime import datetime
from pathlib import Path
import os
import sys
src_path = str(Path(__file__).resolve().parent / "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)
from block_code import extract_title, markdown_to_html_node
# import shutil
# NOTE: replacing shutil scripts sacrifices preservation of copied files' metadata (timestamps) and permissions 

def migrate_files(
    source_folder: str | Path,
    target_folder: str | Path,
) -> tuple[Path, Path]:
    root = Path.cwd().resolve()
    source = (root / source_folder).resolve()
    target = (root / target_folder).resolve()

    # Limit this function to folders directly under the project root.
    if source.parent != root or target.parent != root:
        raise ValueError("Source and target must be folders directly under the project root")
    if source == target:
        raise ValueError("Source and target folders must be different")
    if not source.is_dir():
        raise NotADirectoryError(source)
    if target.exists() and not target.is_dir():
        raise NotADirectoryError(target)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = root / "backups" / f"{target.name}_{timestamp}"
    log_path = root / "execution_logs" / f"file_migration_log_{timestamp}"

    backup.parent.mkdir(parents=True, exist_ok=True)
    if backup.exists() or log_path.exists():
        raise FileExistsError("Backup or log path already exists; try again")
    
# Add helpers to replace shutil based script
    def copy_file(src: Path, dest: Path) -> None:
        # Copy binary data in chunks so large files don't have to fit in memory.
        with src.open("rb") as source_file, dest.open("wb") as dest_file:
            while chunk := source_file.read(1024 * 1024):
                dest_file.write(chunk)


    def delete_item(item: Path, log) -> None:
        if item.is_symlink() or not item.is_dir():
            log.write(f"DELETE FILE {item}\n")
            item.unlink()
            return

        log.write(f"DELETE DIR  {item}\n")
        for child in item.iterdir():
            delete_item(child, log)
        item.rmdir()
# End helpers

    def copy_contents(src_dir: Path, dest_dir: Path, log) -> None:
        for item in sorted(src_dir.iterdir()):
            dest_item = dest_dir / item.name

            if item.is_symlink():
                dest_item.symlink_to(os.readlink(item))
                log.write(f"BACKUP LINK {item} -> {dest_item}\n")
            elif item.is_dir():
                dest_item.mkdir()
                log.write(f"BACKUP DIR  {item} -> {dest_item}\n")
                copy_contents(item, dest_item, log)
            else:
                # shutil.copy2(item, dest_item) # replace shutil script with:
                copy_file(item, dest_item) # end replace
                log.write(f"BACKUP FILE {item} -> {dest_item}\n")

    def copy_source_contents(src_dir: Path, dest_dir: Path, log) -> None:
        for item in sorted(src_dir.iterdir()):
            dest_item = dest_dir / item.name

            if item.is_symlink():
                dest_item.symlink_to(os.readlink(item))
                log.write(f"COPY LINK {item} -> {dest_item}\n")
            elif item.is_dir():
                dest_item.mkdir()
                log.write(f"COPY DIR  {item} -> {dest_item}\n")
                copy_source_contents(item, dest_item, log)
            else:
                #shutil.copy2(item, dest_item) # replace shutil script with:
                copy_file(item, dest_item) # end replace
                log.write(f"COPY FILE {item} -> {dest_item}\n")

    with log_path.open("x", encoding="utf-8") as log:
        backup.mkdir()
        if target.exists():
            copy_contents(target, backup, log)

        target.mkdir(exist_ok=True)

        # Clear the target only after its backup has completed.
        #replace shutil based script
            #for item in target.iterdir():
            #    if item.is_dir() and not item.is_symlink():
            #        log.write(f"DELETE DIR  {item}\n")
            #        shutil.rmtree(item)
            #    else:
            #        log.write(f"DELETE FILE {item}\n")
            #        item.unlink()
        #with:
        for item in target.iterdir():
            delete_item(item, log)

        copy_source_contents(source, target, log)

    return backup, log_path


def generate_page(
    basepath: str | Path,
    from_path: str | Path,
    template_path: str | Path,
    dest_path: str | Path,
) -> None:
    print(
        f"Generating page from {from_path} to {dest_path} "
        f"using {template_path}"
    )

    markdown_path = Path(from_path)
    template_file_path = Path(template_path)
    destination_path = Path(dest_path)

    markdown = markdown_path.read_text(encoding="utf-8")
    template = template_file_path.read_text(encoding="utf-8")

    # The source modules use flat imports, so make src/ importable when this
    # project-root module is run as part of the `src` package.
    # src_path = str(Path(__file__).resolve().parent / "src")
    # if src_path not in sys.path:
    #     sys.path.insert(0, src_path)

#    from block_code import extract_title, markdown_to_html_node

    content = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    page = template.replace("{{ Title }}", title).replace("{{ Content }}", content).replace('href="/', f'href="{basepath}')

    destination_path.parent.mkdir(parents=True, exist_ok=True)
    destination_path.write_text(page, encoding="utf-8")


def generate_pages_recursive(basepath: str,
                             dir_path_content: str | Path, 
                             template_path: str | Path, 
                             dest_dir_path: str | Path,
                             ) -> None:
    
#    from block_code import extract_title, markdown_to_html_node

    root = Path.cwd().resolve()
    source = (root / dir_path_content).resolve()
    template_file = (root / template_path).resolve()
    template_html = template_file.read_text(encoding="utf-8")
    target = (root / dest_dir_path).resolve()

    # Limit this function to folders directly under the project root.
    if source.parent != root or template_file.parent != root or target.parent != root:
        raise ValueError("Content, template and destination must be folders directly under the project root")
    if source == target:
        raise ValueError("Source and target folders must be different")
    if not source.is_dir():
        raise NotADirectoryError(source)
    if not template_file.is_file():
        raise FileNotFoundError(template_file)
    if target.exists() and not target.is_dir():
        raise NotADirectoryError(target)

    print(
        f"Generating pages from {dir_path_content} to {dest_dir_path} "
        f"using {template_path}"
    )

    markdown_path = Path(dir_path_content)
    template_file_path = Path(template_path)
    destination_path = Path(dest_dir_path)

    def generate_from_contents(
        basepath: str | Path,
        from_path: Path,
        template_html: str,
        dest_path: Path,
    ) -> None:
        dest_path.mkdir(parents=True, exist_ok=True)

        for item in sorted(from_path.iterdir()):
            if item.is_dir():
                generate_from_contents(
                    basepath,
                    item,
                    template_html,
                    dest_path / item.name,
                )
            elif item.is_file() and item.suffix.lower() == ".md":
                markdown = item.read_text(encoding="utf-8")
                content = markdown_to_html_node(markdown).to_html()
                title = extract_title(markdown)

                page = (
                    template_html
                    .replace("{{ Title }}", title)
                    .replace("{{ Content }}", content)
                    .replace('href="/', f'href="{basepath}')
                )

                output_path = dest_path / item.with_suffix(".html").name
                output_path.write_text(page, encoding="utf-8")

    generate_from_contents(basepath, source, template_html, target)
