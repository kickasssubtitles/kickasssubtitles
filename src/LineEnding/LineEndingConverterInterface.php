<?php

declare(strict_types=1);

/*
 * KickAssSubtitles source code file
 *
 * @link      https://kickasssubtitles.com
 * @copyright Copyright (c) 2016-2020
 * @author    grzesw <contact@kickasssubtitles.com>
 */

namespace KickAssSubtitles\LineEnding;

use Throwable;

/**
 * Interface LineEndingConverterInterface.
 */
interface LineEndingConverterInterface
{
    const ERR_CONVERSION_FAILED = 'Conversion failed';

    /**
     * @throws Throwable
     */
    public function convert(string $input, LineEnding $from, LineEnding $to): string;

    /**
     * @throws Throwable
     */
    public function convertFile(string $file, LineEnding $from, LineEnding $to): void;
}
