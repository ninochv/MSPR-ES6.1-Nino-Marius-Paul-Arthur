#!/usr/bin/env python3
"""
NTL-SysToolbox - Interface CLI interactive
Outil d'exploitation système pour Nord Transit Logistics
"""

import sys
import os
import argparse
from typing import Optional

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ntl_systoolbox import __version__
from ntl_systoolbox.core import setup_logger, get_logger, Config, OutputFormatter, ExitCode
from ntl_systoolbox.cli.menu import InteractiveMenu
from ntl_systoolbox.cli.commands import CommandHandler


def parse_arguments():
    """Parse les arguments de la ligne de commande."""
    parser = argparse.ArgumentParser(
        prog='ntl-systoolbox',
        description='NTL-SysToolbox - Outil CLI pour Nord Transit Logistics',
        epilog='Utilisez --interactive pour le menu interactif ou spécifiez une commande.'
    )
    
    parser.add_argument(
        '--version', '-v',
        action='version',
        version=f'NTL-SysToolbox v{__version__}'
    )
    
    parser.add_argument(
        '--interactive', '-i',
        action='store_true',
        help='Lancer le menu interactif'
    )
    
    parser.add_argument(
        '--config', '-c',
        type=str,
        default=None,
        help='Chemin vers le fichier de configuration'
    )
    
    parser.add_argument(
        '--output', '-o',
        choices=['human', 'json', 'both'],
        default='both',
        help='Format de sortie (défaut: both)'
    )
    
    parser.add_argument(
        '--log-level', '-l',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        default='INFO',
        help='Niveau de log (défaut: INFO)'
    )
    
    parser.add_argument(
        '--no-color',
        action='store_true',
        help='Désactiver les couleurs dans la sortie'
    )
    
    # Sous-commandes
    subparsers = parser.add_subparsers(dest='command', help='Commandes disponibles')
    
    
    # === Module Sauvegarde ===
    backup_parser = subparsers.add_parser('backup', aliases=['bkp'],
                                          help='Module de sauvegarde WMS')
    backup_sub = backup_parser.add_subparsers(dest='backup_command')
    
    # backup full
    full_parser = backup_sub.add_parser('full', help='Sauvegarde complète de la base')
    full_parser.add_argument('--output', '-o', type=str, help='Chemin du fichier de sortie')
    
    # backup table
    table_parser = backup_sub.add_parser('table', help='Exporter une table en CSV')
    table_parser.add_argument('table_name', type=str, help='Nom de la table à exporter')
    table_parser.add_argument('--output', '-o', type=str, help='Chemin du fichier de sortie')
    table_parser.add_argument('--where', type=str, help='Clause WHERE pour filtrer')
    
    # backup critical
    critical_parser = backup_sub.add_parser('critical', help='Sauvegarder les tables critiques')
    
    # backup verify
    verify_parser = backup_sub.add_parser('verify', help='Vérifier l\'intégrité d\'une sauvegarde')
    verify_parser.add_argument('backup_file', type=str, nargs='?', help='Fichier à vérifier')
    verify_parser.add_argument('--all', action='store_true', help='Vérifier toutes les sauvegardes')
    
    # backup cleanup
    cleanup_parser = backup_sub.add_parser('cleanup', help='Nettoyer les anciennes sauvegardes')
    
    return parser.parse_args()


def main():
    """Point d'entrée principal."""
    args = parse_arguments()
    
    # Initialiser la configuration
    config = Config()
    if args.config:
        config.load(config_path=args.config)
    
    # Initialiser le logger
    log_level = args.log_level or config.get('general', 'log_level', default='INFO')
    log_dir = config.get('general', 'log_dir', default='./logs')
    logger = setup_logger(log_level=log_level, log_dir=log_dir)
    
    # Initialiser le formateur de sortie
    output_format = args.output or config.get('general', 'output_format', default='both')
    use_colors = not args.no_color
    output = OutputFormatter(format_type=output_format, use_colors=use_colors)
    
    # Mode interactif ou commande directe
    if args.interactive or args.command is None:
        # Lancer le menu interactif
        menu = InteractiveMenu(config=config, output=output)
        exit_code = menu.run()
    else:
        # Exécuter la commande
        handler = CommandHandler(config=config, output=output)
        exit_code = handler.execute(args)
    
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
