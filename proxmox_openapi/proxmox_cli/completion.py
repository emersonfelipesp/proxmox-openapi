"""Shell completion support for bash and zsh."""

from __future__ import annotations

from typing import Optional

import typer

from proxmox_openapi.proxmox_cli.app import app

completion_app = typer.Typer(name="completion", help="Shell completion support")


@completion_app.command()
def install_bash() -> None:
    """Install bash completion for proxmox CLI.

    Usage:
        eval "$(_PROXMOX_COMPLETE=bash_source proxmox)"
    """
    completion_script = """
# Bash completion script for proxmox CLI
_proxmox_completion() {
    local cur prev words cword
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"

    # Get available commands
    local commands="get create set-cmd delete ls usage help-cmd"

    # Get global options
    local global_opts="--version --verbose --quiet --config --backend --host --user --password --token-value --port --service --output"

    case "${prev}" in
        --backend)
            COMPREPLY=( $(compgen -W "https ssh_paramiko openssh local mock" -- ${cur}) )
            return 0
            ;;
        --service)
            COMPREPLY=( $(compgen -W "PVE PMG PBS" -- ${cur}) )
            return 0
            ;;
        --output|-o)
            COMPREPLY=( $(compgen -W "json yaml table text auto" -- ${cur}) )
            return 0
            ;;
    esac

    # First word is command
    if [[ ${COMP_CWORD} -eq 1 ]]; then
        COMPREPLY=( $(compgen -W "${commands}" -- ${cur}) )
    else
        # Subsequent words might be paths or options
        COMPREPLY=( $(compgen -W "${global_opts}" -- ${cur}) )
    fi
}

complete -F _proxmox_completion proxmox
"""
    typer.echo(completion_script)


@completion_app.command()
def install_zsh() -> None:
    """Install zsh completion for proxmox CLI.

    Usage:
        eval "$(_PROXMOX_COMPLETE=zsh_source proxmox)"
    """
    completion_script = """
#compdef proxmox

_proxmox() {
    local curcontext="$curcontext" state ret=1
    local -a commands
    
    commands=(
        'get:Retrieve resources from the Proxmox API'
        'create:Create resources in the Proxmox API'
        'set-cmd:Update resources in the Proxmox API'
        'delete:Delete resources from the Proxmox API'
        'ls:List child resources at a given path'
        'usage:Show API schema and usage information'
        'help-cmd:Show help for API endpoints'
    )
    
    local -a global_opts=(
        '(--version)--version[Show version and exit]'
        '(-v --verbose)--verbose[Enable verbose logging]'
        '(-q --quiet)--quiet[Suppress non-essential output]'
        '(-c --config)--config=[Path to configuration file]:config file:_files'
        '(-b --backend)--backend=[Backend to use]:backend:(https ssh_paramiko openssh local mock)'
        '(-H --host)--host=[Proxmox host address]:host:'
        '(-U --user)--user=[Username or token name]:user:'
        '(-P --password)--password=[Password]:password:'
        '--token-value=[API token value]:token:'
        '--port=[API port]:port:'
        '(-S --service)--service=[Proxmox service type]:service:(PVE PMG PBS)'
        '(-o --output)--output=[Output format]:format:(json yaml table text auto)'
    )
    
    _arguments $global_opts '*::command:->cmd' && return
    
    case $state in
        cmd)
            _describe commands commands
            ;;
    esac
}

_proxmox
"""
    typer.echo(completion_script)


@app.command()
def completion_install(shell: str = typer.Option("bash", help="Shell type (bash or zsh)")) -> None:
    """Install shell completion for proxmox CLI.

    Examples:
        # Bash
        proxmox completion-install --shell bash >> ~/.bashrc

        # Zsh
        proxmox completion-install --shell zsh >> ~/.zshrc
    """
    if shell == "bash":
        typer.invoke(install_bash)
    elif shell == "zsh":
        typer.invoke(install_zsh)
    else:
        typer.echo(f"Unknown shell: {shell}", err=True)
        raise typer.Exit(code=1)
