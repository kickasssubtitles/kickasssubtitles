<?php

declare(strict_types=1);

/*
 * KickAssSubtitles source code file
 *
 * @link      https://kickasssubtitles.com
 * @copyright Copyright (c) 2016-2020
 * @author    grzesw <contact@kickasssubtitles.com>
 */

namespace KickAssSubtitles\Storage;

use Throwable;

/**
 * Interface HasStorageInterface.
 */
interface HasStorageInterface
{
    /**
     * @throws Throwable
     */
    public function getStorage(): StorageInterface;

    public function setStorage(StorageInterface $storage): void;

    /**
     * @throws Throwable
     */
    public function tearDownStorage(): void;
}
